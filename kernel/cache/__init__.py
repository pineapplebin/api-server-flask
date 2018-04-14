import pickle
from redis import StrictRedis
from redis.client import StrictPipeline
from .utils import CacheKey
from .decorators import using_cache


def _unpickle(data):
    try:
        return pickle.loads(data) if data else None
    except pickle.UnpicklingError as err:
        return data


def _pickle(data):
    return pickle.dumps(data)


class CacheProxy:
    def __init__(self, app):
        redis_config = {
            'host': app.config.get('REDIS_HOST', 'localhost'),
            'port': app.config.get('REDIS_PORT', 6379),
            'db': app.config.get('REDIS_DB', 0),
            'password': app.config.get('REDIS_PASS', None),
        }
        self.default_ex = app.config.get('REDIS_DEFAUTL_EX', None)
        self.client = StrictRedis(**redis_config)

    # 事务
    def pipeline(self, *args, **kwargs) -> StrictPipeline:
        return self.client.pipeline(*args, **kwargs)

    # 键值
    def get(self, name):
        return _unpickle(self.client.get(str(name)))

    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        return self.client.set(str(name), pickle.dumps(value),
                               ex or self.default_ex, px, nx, xx)

    def delete(self, *names):
        return self.client.delete(*map(str, names))

    def expire(self, name, time):
        return self.client.expire(str(name), time)

    def persist(self, name):
        return self.client.persist(str(name))

    def ttl(self, name):
        return self.client.ttl(str(name))

    def keys(self, pattern='*'):
        return [k.decode('utf-8')
                for k in self.client.keys(str(CacheKey(pattern)))]

    # bit
    def bitcount(self, name, start=None, end=None):
        return self.client.bitcount(str(name), start=start, end=end)

    def setbit(self, name, offset, value):
        return self.client.setbit(str(name), offset=offset, value=value)

    # 数字
    def nget(self, name) -> int:
        rst = self.client.get(str(name))
        return int(rst) if rst is not None else None

    def nset(self, name, value: int, ex=None, px=None, nx=False, xx=False):
        return self.client.set(str(name), str(value),
                               ex or self.default_ex, px, nx, xx)

    def ndecr(self, name, amount: int = 1) -> int:
        return self.client.decr(str(name), amount)

    def nincr(self, name, amount: int = 1) -> int:
        return int(self.client.incr(str(name), amount))

    # 列表
    def lrange(self, name, start, end) -> tuple:
        return tuple(map(_unpickle, self.client.lrange(str(name), start, end)))

    def rpush(self, name, *values):
        return self.client.rpush(str(name), *map(_pickle, values))

    def lpop(self, name):
        return _unpickle(self.client.lpop(str(name)))

    def llen(self, name):
        return self.client.llen(str(name))
