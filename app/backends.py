from flask import current_app, request
from kernel.auth import encode_token, decode_token, BannedUser
from kernel.auth.backends import AbstractBackend

from .controllers.user.dal import get_user_by_id


class Backend(AbstractBackend):
    NAME = 'Backend'
    SALT = 'backend'

    @classmethod
    def handle(cls):
        token = request.headers.get('Authorization', None)
        if not token:
            return None
        # 检验token
        decoded = cls.decode(token)
        if not decoded or not isinstance(decoded, dict) or (
                'user_id' not in decoded):
            return None
        # 检查用户
        user = get_user_by_id(id=decoded['user_id'])

        if user.is_banned:
            user = BannedUser(user)

        return user or None

    @classmethod
    def decode(cls, token: str) -> dict:
        secret = current_app.config.get('SECRET_KEY', '') + cls.SALT
        return decode_token(secret, token)

    @classmethod
    def encode(cls, payload: dict) -> str:
        secret = current_app.config.get('SECRET_KEY', '') + cls.SALT
        return encode_token(secret, payload)
