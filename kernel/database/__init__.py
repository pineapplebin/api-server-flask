import datetime
from flask_sqlalchemy import SQLAlchemy
from .access_layer import AccessLayer

DB = SQLAlchemy()


def _is_type(typu: str, target):
    assert hasattr(DB, typu), 'Type {0} does not exists'.format(typu)
    return isinstance(target.type, getattr(DB, typu))


class BaseHelper:
    __model__ = None
    __subclassess__ = {}

    def __init__(self, model_instance=None, serialize_dict=None):
        """
        将数据对象实例或字典数据转换成Helper对象
        用于统一给逻辑层处理或执行业务行为用的结构

        目前会根据Model层定义的relationship把相应的关系数据也转换成相应的Helper对象
        列表结构也支持

        :param model_instance: SQLAlchemy查询得到的对象实例
        :param serialize_dict: json.loads得到的字典型数据
        """
        assert model_instance or serialize_dict, (
            'BaseHelper.__init__ required "model_instance" or "serialize_dict"')

        self_name = self.__model__.__name__
        for name, field in self.__class__._get_columns():
            if model_instance:
                assert hasattr(model_instance, name), (
                    '{0} model does not have attribute {1}'.format(
                        self_name, name))
                value = getattr(model_instance, name)
            else:
                assert name in serialize_dict, (
                    '{0} dict does not have key {1}'.format(self_name, name))
                value = serialize_dict.get(name)

            if _is_type('DateTime', field) and not isinstance(
                    value, datetime.datetime):
                if value is not None:
                    value = datetime.datetime.fromtimestamp(value)

            setattr(self, name, value)

        for name, _ in self.__class__._get_relationships():
            model_name = getattr(
                self.__model__, name).property.mapper.class_.__name__
            # helper = getattr(HELPERS, model_name)
            helper = self.__subclassess__.get(model_name)
            if model_instance:
                # assert hasattr(model_instance, name), (
                #     '{0} model does not have relation {1}'.format(self_name,
                #                                                   name))
                relationship = getattr(model_instance, name, None)
                if isinstance(relationship, DB.Model):
                    value = helper(model_instance=relationship)
                elif isinstance(relationship, (list, tuple)):
                    value = list(map(
                        lambda o: helper(model_instance=o), relationship))
                else:
                    value = None
            else:
                # assert name in serialize_dict, (
                #     '{0} dict does not have relation {1}'.format(self_name,
                #                                                  name))
                relationship = serialize_dict.get(name, None)
                if isinstance(relationship, dict):
                    value = helper(serialize_dict=relationship)
                elif isinstance(relationship, (list, tuple)):
                    value = list(
                        map(lambda d: helper(serialize_dict=d), relationship))
                else:
                    value = None

            setattr(self, name, value)

    @classmethod
    def get_model(cls) -> DB.Model:
        return cls.__model__

    @classmethod
    def _get_columns(cls):
        return cls.__model__.__table__.columns.items()

    @classmethod
    def _get_relationships(cls):
        return cls.__model__.__mapper__.relationships.items()

    @classmethod
    def deserialize(cls, **kwargs):
        return cls(serialize_dict=kwargs)

    def serialize(self, include_relationship=False) -> dict:
        d = dict()
        for name, field in self._get_columns():
            value = getattr(self, name, None)
            if _is_type('DateTime', field):
                value = value.timestamp() if value else None
            d[name] = value

        if include_relationship:
            for name, _ in self._get_relationships():
                value = getattr(self, name, None)
                if isinstance(value, BaseHelper):
                    d[name] = value.serialize(
                        include_relationship=include_relationship)
                elif isinstance(value, (list, tuple)):
                    d[name] = list(map(lambda h: h.serialize(
                        include_relationship=include_relationship), value))

        return d

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__subclassess__[cls.__model__.__name__] = cls
