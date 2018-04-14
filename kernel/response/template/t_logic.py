from .utils import get_value, missing_


class LogicParseException(Exception):
    pass


class TLogic:
    """ 模板逻辑模块基类 """

    def parse(self, render_, **kwargs) -> list:
        raise NotImplementedError()

    @property
    def __dict__(self):
        return '<{0}>'.format(self.__class__.__name__)


class THolder(TLogic):
    """ 模板占位符
    usage:
        template = {
            'user': {
                'id': THolder('user.id')
            }
        }
        render(template, user=dict(id=1))

        # {'user': {'id': 1}}
    """

    def __init__(self, key, default=missing_):
        assert isinstance(key, str) and len(key), 'key must be string'

        self.key = key
        self.default = default

    def parse(self, render_, **kwargs):
        return get_value(self.key, kwargs, self.default)

    @property
    def __dict__(self):
        return '<{0}>'.format(self.key)


class TFor(TLogic):
    """ 循环逻辑
    usage:
        template = {
            'events': TFor({
                'id': THolder('event.id')
            }, 'events', prefix='event')
        }
        render(template, events=[dict(id=1), dict(id=2)])

        # {'events': [{'id': 1}, {'id': 2}]
    """

    def __init__(self, template, key: str, prefix='for', getter=None):
        """ 初始化一个循环逻辑模板

        :param template: 遍历内容的输出模板
        :param key: 对应可遍历的参数的key
        :param prefix: 输出模板中的对象前缀
        :param getter: 可指定遍历内容的某个属性或处理函数，为None则为遍历内容自身
        """
        self.template = template
        self.key = key
        self.prefix = prefix
        self.getter = getter

    def parse(self, render_, **kwargs) -> list:
        data = get_value(self.key, kwargs)
        assert isinstance(data, (list, tuple)), 'TFor required a iterable data'

        # output = []
        # for d in data:
        #     result = render_(self.template, **{self.prefix: d}, **kwargs)
        #     output.append(result)
        #
        # return output
        return [render_(self.template,
                        **{self.prefix: self.getter(d) if self.getter else d},
                        **kwargs)
                for d in data]

    @property
    def __dict__(self):
        return [self.template]


class TEnum(TLogic):
    def __init__(self, key, enum: tuple, default=missing_):
        assert isinstance(key, str) and len(key), 'key must be string'
        assert isinstance(enum, (tuple, list)), 'enum must be iterable'

        self.enum = enum
        self.key = key
        self.default = default

    def parse(self, render_, **kwargs):
        value = get_value(self.key, source=kwargs)
        if value not in self.enum:
            raise LogicParseException(
                'value "{0}" is not in "{1}"'.format(value, self.enum))
        return value

    @property
    def __dict__(self):
        return '|'.join(map(lambda o: str(o), self.enum))


class TDict(TLogic):
    def __init__(self, template, show_key, key,
                 prefix='dict', default=missing_):
        self.show_key = show_key
        self.template = template
        self.key = key
        self.prefix = prefix

    def parse(self, render_, **kwargs):
        value = get_value(self.key, source=kwargs)
        assert isinstance(value, dict), 'TDict required a dict type value'

        return {k: render_(self.template, **{self.prefix: v}, **kwargs)
                for k, v in value.items()}

    @property
    def __dict__(self):
        return {self.show_key: self.template}
