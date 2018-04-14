from .utils import get_accessor


class AccessLayer:
    def __init__(self, helper):
        self.clazz = {
            'helper': helper,
            'model': helper.get_model()
        }

    def create(self):
        def decorate(fn):
            def wrap(**kwargs):
                db, _ = get_accessor()
                instance = self.clazz['model'](**kwargs)
                db.session.add(instance)
                db.session.commit()
                helper = self.clazz['helper'](instance)
                rst = fn(**kwargs, instance=instance, helper=helper)
                return rst

            return wrap

        return decorate

    def retrieve(self):
        def decorate(fn):
            def wrap(**kwargs):
                pass

        return decorate

    def update(self):
        def decorate(fn):
            def wrap(*args, **kwargs):
                pass

        return decorate

    def delete(self):
        def decorate(fn):
            def wrap(*args, **kwargs):
                pass

        return decorate
