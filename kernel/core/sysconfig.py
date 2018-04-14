def _filter_attribute(attr: str):
    return not attr.startswith('_') and attr != 'to_dict'


class SysConfig:
    # system
    DEBUG = False
    TESTING = False
    ENVIRONMENT = 'default'
    SECRET_KEY = ''
    JWT_SECRET = ''
    APP_NAME = ''

    # kernel
    AUTH_BACKENDS = []

    MAX_CONTENT_LENGTH = 1048576
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

    LOG_FILE_NAME = 'logs/server.log'
    LOG_FORMAT = ("\n%(levelname)s - %(asctime)s - in %(module)s "
                  "[%(pathname)s:%(lineno)d]:\n%(message)s\n")

    # database
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_PASS = None
    REDIS_DB = 0
    REDIS_DEFAUTL_EX = None

    def to_dict(self) -> dict:
        return {k: getattr(self, k) for k in dir(self) if _filter_attribute(k)}
