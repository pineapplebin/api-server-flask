from kernel.core.sysconfig import SysConfig


class Config(SysConfig):
    DEBUG = True
    AUTH_BACKENDS = [
        'app.backends.Backend'
    ]

    SQLALCHEMY_DATABASE_URI = ("postgresql://flask:123456@db:5432/flask")
    REDIS_HOST = 'db'


configs = {
    'default': Config(),
}
