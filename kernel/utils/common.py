import datetime
import random
import json
from typing import Callable, Iterable, TypeVar

T = TypeVar('T')
RANDOM_BASE = [
    '0123456789',
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
]


def to_seconds(*, hours=0, minutes=0, seconds=0) -> int:
    """
    >>> to_seconds(hours=1, minutes=1)
    3660
    >>> to_seconds(minutes=1, seconds=10)
    70
    """
    assert isinstance(hours, int), TypeError
    assert isinstance(minutes, int), TypeError
    assert isinstance(seconds, int), TypeError
    return hours * 3600 + minutes * 60 + seconds


def indexof(fn: Callable[[T], bool], iterable: Iterable[T]) -> int:
    """ 根据处理函数查找是否存在元素
    如果存在满足条件的元素则返回下标，否则返回-1

    >>> indexof(lambda n: n == 2, range(10))
    2
    >>> indexof(lambda n: n > 10, range(10))
    -1

    :param fn: 处理函数
    :param iterable: 可迭代的数据
    :return: 结果下标
    """
    for idx, el in enumerate(iterable):
        rst = fn(el)
        if rst:
            return idx
    return -1


def addattr(obj, attr, value):
    """ 为对象添加属性并返回对象

    :param obj: 对象
    :param attr: 属性名
    :param value: 值
    :return: 对象
    """
    setattr(obj, attr, value)
    return obj


def randomstr(length: int = 6, base: str = 'number') -> str:
    """ 生成随机字符串

    :param length:
    :param base: 随机范围，枚举(number, letter, both)
    :return:
    """
    _base = {
        'number': RANDOM_BASE[0],
        'letter': RANDOM_BASE[1],
        'both': RANDOM_BASE[1] + RANDOM_BASE[0]
    }[base]
    return ''.join([str(random.choice(_base)) for _ in range(length)])


def jsonformat(**kwargs):
    return json.dumps(kwargs, indent=2)


def timedelta_to_zero() -> datetime.timedelta:
    now = datetime.datetime.now()
    next_zero = datetime.datetime(
        year=now.year, month=now.month, day=now.day) + datetime.timedelta(
        days=1)
    return next_zero - now


def datetimestring(dt: datetime.datetime = None) -> str:
    if not dt:
        dt = datetime.datetime.now()
    return f'{dt.year}-{dt.month}-{dt.day}'
