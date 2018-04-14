from importlib import import_module


def import_instance(path: str):
    splits = path.rsplit('.', 1)
    module = import_module(splits[0])
    if len(splits) != 2 or not hasattr(module, splits[1]):
        raise ValueError('invalid import path: ' + path)

    return getattr(module, splits[1])
