from datetime import datetime

missing_ = {'@@missing': True}


def _parse_path(path):
    return path.split('.')


def get_value(path, source, default=missing_):
    path_list = _parse_path(path)
    value = source
    for key in path_list:
        if isinstance(value, dict):
            if key not in value:
                if default == missing_:
                    raise Exception(
                        'path "{0}" is not exists in dict'.format(path))
                else:
                    value = default
                    break
            else:
                value = value[key]
        elif isinstance(value, object):
            if not hasattr(value, key):
                if default == missing_:
                    raise Exception(
                        'path "{0}" is not exists in object'.format(path))
                else:
                    value = default
                    break
            else:
                value = getattr(value, key)
        else:
            raise TypeError(
                '{0} is invalid type: {1}'.format(value, type(value)))

    if isinstance(value, datetime):
        value = value.timestamp()

    return value
