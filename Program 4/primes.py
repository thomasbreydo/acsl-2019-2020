import functools
import math


@functools.lru_cache(maxsize=None)  # memoize
def isprime(x):
    if x <= 1:
        return False
    if x == 2:
        return True
    for i in range(2, math.ceil(math.sqrt(x)) + 1):
        if isprime(i) and x % i == 0:
            return False
    return True
