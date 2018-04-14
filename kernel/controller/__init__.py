import json
from functools import wraps
from flask import Blueprint, g, abort, current_app
from webargs import ValidationError
from webargs.flaskparser import FlaskParser

from kernel.auth import current_user, BannedUser
from kernel.auth.backends import AbstractBackend
from kernel.cache import CacheKey

from .defaults import StatusCode, STATUS_TEXT


class BaseController:
    REQUIRED_ENV = None
    AUTH_BACKEND = None

    def __init__(self, import_name, name, prefix, template_folder=None):
        self.blueprint = Blueprint(import_name=import_name, name=name,
                                   url_prefix=prefix,
                                   template_folder=template_folder)
        self.prefix = prefix
        self.name = name
        self.parser = FlaskParser()
        self.apidoc = {}

        @self.parser.error_handler
        def _handle_error(err):
            raise err

    def bind(self, core):
        """ 将该controller绑定到app上，并注册相关事件 """
        app = core.app
        if self.REQUIRED_ENV:
            env = app.config['ENVIRONMENT']
            if env != self.REQUIRED_ENV:
                return False
        app.register_blueprint(self.blueprint)
        return True

    def _using_apidoc(self, fn):
        """ 判断当前视图函数是否开启apidoc """
        name = getattr(fn, '__name__', None)
        return name in self.apidoc

    def _route(self, route, method, **options):
        """ 绑定视图函数到blueprint上 """

        def decorator(fn):
            # 检查apidoc
            if self._using_apidoc(fn):
                doc = self.apidoc[fn.__name__]
                doc['method'] = method
                doc['route'] = self.prefix + route

            options['methods'] = [method]
            return self.blueprint.route(route, **options)(fn)

        return decorator

    def get(self, route, **options):
        return self._route(route, 'GET', **options)

    def post(self, route, **options):
        return self._route(route, 'POST', **options)

    def login_required(self):
        """ 校验存在已验证用户
        如果检查到user为BannedUser的实例时，意味着用户被禁止访问
        """

        def decorator(fn):
            @wraps(fn)
            def wrap(*args, **kwargs):
                if not current_user:
                    return self.handle_unauthorization()

                if isinstance(self.AUTH_BACKEND, str):
                    backend = self.AUTH_BACKEND
                elif isinstance(self.AUTH_BACKEND, type) and issubclass(
                        self.AUTH_BACKEND, AbstractBackend):
                    backend = self.AUTH_BACKEND.NAME
                else:
                    backend = str(self.AUTH_BACKEND)
                if getattr(g, 'backend', None) and self.AUTH_BACKEND:
                    if g.backend != backend:
                        return self.handle_unauthorization()

                if isinstance(current_user, BannedUser):
                    return self.handle_banned_user()

                return fn(*args, **kwargs)

            return wrap

        return decorator

    def visit_limit(self, seconds):
        """ 访问限制
        根据通过验证的user id作为key一部分，所以要使用在login_required之后
        """

        def decorator(fn):
            @wraps(fn)
            def wrap(*args, **kwargs):
                if not current_user:
                    return self.handle_unauthorization()

                cache = current_app.core.cache
                user_id = current_user.id
                fn_key = f'{self.name}_{fn.__name__}'
                key = CacheKey('visit_limit', user_id, fn_key)

                if cache.nget(key):
                    if cache.ttl(key) == -1:
                        cache.expire(key, seconds)
                    return self.handle_visit_limit()

                rst = cache.nincr(key)
                cache.expire(key, seconds)
                if rst > 1:
                    return self.handle_visit_limit()

                return fn(*args, **kwargs)

            return wrap

        return decorator

    def use_args(self, fields, code, validate=None, location='form'):
        """ 校验请求参数

        :param fields: 检验字段
        :param code: 检验错误时错误码
        :param validate: 对整个表单的校验
        :param location: 检验参数所在位置（form, query, json, headers...）
        :return:
        """
        assert location in ['query', 'form'], \
            'location should use "query" or "form"'

        def decorator(fn):
            # 检查apidoc
            if self._using_apidoc(fn):
                _args = self.apidoc[fn.__name__].get('args', {})
                _location = _args.get(location, {})
                _location.update(fields)
                _args[location] = _location
                self.apidoc[fn.__name__]['args'] = _args
                self._add_error_info(code, fn.__name__)

            @wraps(fn)
            def wrap(*args, **kwargs):
                try:
                    result = self.parser.parse(
                        fields, validate=validate,
                        locations=('querystring', 'form', 'json'))
                    if 'parsed' in kwargs:
                        old = kwargs.pop('parsed')
                        old.update(result)
                        result = old
                    return fn(parsed=result, *args, **kwargs)
                except ValidationError as err:
                    return self.handle_bad_arguments(err.messages)

            return wrap

        return decorator

    def add_apidoc(self, errors=None, response=None):
        """ 开启api文档

        :param errors: controller自身会自动添加一部分信息于errors中
        :param response: 请求成功后返回的格式
        """

        def decorator(fn):
            response_doc = response or {}
            response_doc['code'] = 0

            api_name = fn.__name__
            self.apidoc[api_name] = {
                'doc': fn.__doc__ or '',
                'errors': errors or dict(),
                'response': json.dumps(
                    response_doc, indent=2, sort_keys=True,
                    default=lambda o: o.__dict__)
            }
            return fn

        return decorator

    def format_doc(self):
        """ 格式化文档数据 """
        _formatted = {}
        for view_name, doc_map in self.apidoc.items():
            # 处理args
            args = {}
            temp = dict(**doc_map)
            if 'args' in doc_map:
                for location, fields in doc_map['args'].items():
                    args[location] = {}
                    for arg_name, arg_field in fields.items():
                        args[location][arg_name] = {
                            'type': arg_field.__class__.__name__,
                            'required': getattr(arg_field, 'required', False)
                        }
            temp['args'] = args
            # 处理注释
            doc_text = doc_map.get('doc', '').split('\n')
            temp['doc'] = list(filter(lambda t: len(t),
                                      [t.strip() for t in doc_text]))
            _formatted[view_name] = temp
        return _formatted

    def _add_error_info(self, error_code, api_name):
        """ 自动添加部分错误信息 """
        errors = self.apidoc[api_name]['errors']
        if error_code not in errors:
            errors[error_code] = self.handle_get_error_text(error_code)

    # custom handler
    def handle_unauthorization(self, msg=None):
        return abort(401)

    def handle_bad_arguments(self, msg=None):
        return abort(422)

    def handle_visit_limit(self, msg=None):
        return abort(403)

    def handle_banned_user(self, msg=None):
        return abort(403)

    def handle_get_error_text(self, code):
        return STATUS_TEXT.get(code, 'error')
