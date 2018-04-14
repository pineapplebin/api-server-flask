from flask import jsonify

from .template import *
from .template.utils import get_value


class Response:
    @classmethod
    def _jsonify(cls, **kwargs):
        return jsonify(dict(**kwargs))

    @classmethod
    def raw(cls, code=0, **kwargs):
        assert isinstance(code, int), 'code should be a integer'
        return cls._jsonify(code=code, **kwargs)

    @classmethod
    def render(cls, template_, **kwargs):
        result = render(template_, **kwargs)
        if 'code' not in result:
            result['code'] = 0
        return cls._jsonify(**result)
