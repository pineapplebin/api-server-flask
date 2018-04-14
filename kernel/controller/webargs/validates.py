from webargs import ValidationError


def limit_length(lower=None, upper=None):
    def validate(field):
        length = len(field)
        return (lower <= length if lower else True) and \
               (upper >= length if upper else True)

    return validate


def limit_value(lower=None, upper=None):
    def validate(field):
        value = field
        return (lower <= value if lower else True) and \
               (upper >= value if upper else True)

    return validate


def in_(collection):
    def validate(field):
        return field in collection

    return validate


def not_(fn):
    def validate(field):
        try:
            result = fn(field)
            return not bool(result)
        except ValidationError:
            return True

    return validate


def or_(*fns):
    def validate(field):
        results = []
        for fn in fns:
            try:
                results.append(fn(field))
            except ValidationError:
                results.append(False)
        return any(results)

    return validate
