from flask import _request_ctx_stack, g, request
from kernel.utils.systems import import_instance


class Authenticate:
    def __init__(self, app):
        backends = app.config.get('AUTH_BACKENDS', [])
        assert isinstance(backends, list)
        self.backends = []
        for b in backends:
            self.backends.append(import_instance(b))

    def reload_user(self):
        ctx = _request_ctx_stack.top
        for be in self.backends:
            user = be.handle()
            if user:
                g.backend = be.NAME
                ctx.user = user
                return
        ctx.user = None
