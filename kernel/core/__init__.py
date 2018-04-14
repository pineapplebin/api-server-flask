from importlib import import_module
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS

from kernel.auth.authenticate import Authenticate
from kernel.database import DB
from kernel.cache import CacheProxy

from .sysconfig import SysConfig
from .initialize import init_config, init_event

__all__ = ['SysConfig', 'Core']


def _load_module(import_name, module_name, attrbutes=None):
    module = import_module(import_name + '.' + module_name)
    for name, typi in attrbutes.items() if attrbutes else {}:
        if not hasattr(module, name) or not isinstance(
                getattr(module, name), typi):
            raise Exception(f"{module_name} module must contain a "
                            f"{str(typi)} type '{name}'")
    return module


class Core:
    def __init__(self, import_name: str, config: dict):
        self.app = Flask(import_name)
        self.app.config.update(config)
        self.app.core = self
        self.plugins = {}

        # init database
        DB.init_app(self.app)
        self.db = DB
        self.migrate = Migrate(app=self.app, db=self.db)
        # init authenticate
        self.authenticate = Authenticate(self.app)
        # init redis
        self.cache = CacheProxy(self.app)
        # init cors
        self.cors = CORS(self.app)
        # init others
        init_config(self)
        init_event(self)

        controllers = _load_module(
            import_name, 'controllers', {'controllers': list})
        for c in controllers.controllers:
            self.bind_controller(c)

    def bind_controller(self, controller):
        controller.bind(self)

    def add_plugin(self, key, plugin):
        self.plugins[key] = plugin
        return self

    def get_plugin(self, key):
        assert key in self.plugins, 'plugin "{}" not exists'.format(key)
        return self.plugins[key]
