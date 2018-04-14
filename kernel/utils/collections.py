def notnonedict(**kwargs):
    """
    返回一个不包含值为None的字典

    Example:
    >>> notnonedict(**{'a': 0, 'b': None})
    {'a': 0}
    >>> notnonedict(a=1, b=2)
    {'a': 1, 'b': 2}
    >>> notnonedict(a=None, b=None)
    {}
    """
    return {k: v for k, v in kwargs.items() if v is not None}


def mergedict(*dicts: dict) -> dict:
    """
    合并多个字典，并将得到的新字典返回

    Example:
    >>> mergedict({'a': 1}, {'a': 2}, {'b': 3})
    {'a': 2, 'b': 3}
    """
    rst = {}
    for d in dicts:
        rst.update(d)
    return rst
