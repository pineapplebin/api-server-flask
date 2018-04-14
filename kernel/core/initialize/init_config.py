from logging import (StreamHandler, Formatter, INFO, WARNING)
from logging.handlers import TimedRotatingFileHandler


def init_config(core):
    app = core.app
    config: dict = app.config
    # LOG_FORMAT
    _init_log_format(app, config)


def _init_log_format(app, config):
    if not config.get('LOG_FORMAT', None):
        return
    elif config.get('TESTING', False):
        return

    app.logger.setLevel(INFO)

    fmt = config['LOG_FORMAT']
    formatter = Formatter(fmt)
    for h in app.logger.handlers:
        if isinstance(h, StreamHandler):
            h.setLevel(INFO)
            h.setFormatter(formatter)

    file_handler = TimedRotatingFileHandler(
        config['LOG_FILE_NAME'], when='midnight')
    file_handler.suffix = '%Y-%m-%d.log'
    file_handler.setLevel(WARNING)
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
