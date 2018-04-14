from flask import current_app


class Holder:
    def __str__(self):
        return '{}'

    def __call__(self, name):
        return self


class CacheKey:
    HOLDER = Holder()

    def __init__(self, *args):
        self.holder_count = len(list(filter(
            lambda a: isinstance(a, Holder), args)))
        self.args = [str(a) for a in args]

    def format(self, *args):
        if self.holder_count != len(args):
            raise ValueError('holder amount and arguments amount is not equal')

        name = current_app.config.get('APP_NAME', None)
        return ':'.join([name, *self.args] if name else self.args).format(*args)

    def __str__(self):
        return self.format()

    def __repr__(self):
        return ':'.join(self.args)
