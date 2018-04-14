from collections import namedtuple
from flask import current_app
from redis import WatchError

UsingCache = namedtuple('UsingCache', ['normal', 'list', 'list_add'])


def using_cache_normal(key, names: list = None, ex=None, persist=False):
    def decorator(fn):
        def wrap(**kwargs):
            cache = current_app.core.cache
            k = key.format(*[kwargs[n] for n in (names or [])])
            cached = cache.get(k)
            if cached is not None:
                return cached
            rst = fn(**kwargs)
            if rst is not None:
                cache.set(k, rst, ex=ex)
                if persist:
                    cache.persist(k)
            return rst

        return wrap

    return decorator


def using_cache_list(key, names):
    def decorator(fn):
        def wrap(*, start=0, end=-1, **kwargs):
            cache = current_app.core.cache
            k = key.format(*[kwargs[n] for n in names])
            is_expired = cache.ttl(k) < 1
            if not is_expired:
                return cache.lrange(k, start, end)
            rst = fn(**kwargs, start=start, end=end)
            if not len(rst):
                return rst
            with cache.pipeline() as pipe:
                try:
                    pipe.watch(k)
                    cache.delete(k)
                    cache.rpush(k, *rst)
                    cache.expire(k, cache.default_ex)
                except WatchError:
                    pass
            return rst

        return wrap

    return decorator


def using_cache_list_add(key, names):
    def decorator(fn):
        def wrap(**kwargs):
            rst = fn(**kwargs)
            cache = current_app.core.cache
            k = key.format(*[kwargs[n] for n in names])
            is_expired = cache.ttl(k) < 3
            if not is_expired:
                cache.rpush(k, rst)
            return rst

        return wrap

    return decorator


using_cache = UsingCache(normal=using_cache_normal, list=using_cache_list,
                         list_add=using_cache_list_add)
