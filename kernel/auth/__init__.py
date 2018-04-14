import jwt
from flask import (has_request_context, _request_ctx_stack, current_app)
from werkzeug.local import LocalProxy

current_user = LocalProxy(lambda: _get_user())


def _get_user():
    if has_request_context() and not hasattr(_request_ctx_stack.top, 'user'):
        current_app.core.authenticate.reload_user()

    return getattr(_request_ctx_stack.top, 'user', None)


def encode_token(secret, payload: dict):
    assert payload is not None
    return jwt.encode(payload, secret, algorithm='HS256').decode('utf8')


def decode_token(secret, token):
    try:
        return jwt.decode(token, secret, algorithms=['HS256'])
    except jwt.DecodeError as err:
        return None


class BannedUser:
    def __init__(self, user_data):
        self.user_data = user_data
