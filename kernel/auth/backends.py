class AbstractBackend:
    NAME = None
    SALT = None

    @classmethod
    def handle(cls):
        raise NotImplementedError()
