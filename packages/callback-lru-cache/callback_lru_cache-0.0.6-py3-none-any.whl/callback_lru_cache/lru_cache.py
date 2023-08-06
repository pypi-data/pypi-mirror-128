from functools import wraps
from collections import OrderedDict
from threading import RLock


def lru_cache(maxsize, evict_callback=None):
    def decorator(func):
        cache = OrderedDict()
        lock = RLock()

        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = hash(*args, **kwargs)
            with lock:
                if cache_key in cache:
                    val = cache.pop(cache_key)
                    cache[cache_key] = val
                    return val
                elif len(cache) == maxsize:
                    new_value = func(*args, **kwargs)
                    old_key, old_value = cache.popitem(last=False)
                    if evict_callback is not None:
                        evict_callback(old_key, old_value)
                    cache[cache_key] = new_value
                    return new_value
                else:
                    new_value = func(*args, **kwargs)
                    cache[cache_key] = new_value
                    return new_value

        return wrapper

    return decorator
