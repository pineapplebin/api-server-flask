import json
import marshmallow as ma
from datetime import datetime
from webargs import fields

__all__ = [
    'Str', 'Int', 'Bool', 'List', 'DelimitedList', 'Nested', 'Timestamp'
]

Str = fields.Str
Float = fields.Float
Int = fields.Int
Bool = fields.Bool
List = fields.List
DelimitedList = fields.DelimitedList
Nested = fields.Nested
Url = fields.Url


class JSONStringifyList(ma.fields.List):
    default_error_messages = {
        'invalid': 'Not a jsonstringify list'
    }

    def __init__(self, cls_or_instance, **kwargs):
        super(JSONStringifyList, self).__init__(cls_or_instance, **kwargs)

    def _deserialize(self, value, attr, data):
        try:
            res = json.loads(value[0])
            return super(JSONStringifyList, self)._deserialize(res, attr, data)
        except json.JSONDecodeError:
            return self.fail('invalid')


class Timestamp(ma.fields.Field):
    default_error_messages = {
        'invalid': 'Not a valid timestamp'
    }

    def __init__(self, is_seconds=True, **kwargs):
        self.is_seconds = is_seconds
        super(Timestamp, self).__init__(**kwargs)

    def _format_timestamp(self, value):
        if value is None:
            return None
        try:
            _v = float(value) * (1000 if not self.is_seconds else 1)
            d = datetime.fromtimestamp(_v)
            return d
        except Exception as err:
            print(err)
            return self.fail('invalid')

    def _serialize(self, value, attr, obj):
        return float(value)

    def _deserialize(self, value, attr, obj):
        return self._format_timestamp(value)
