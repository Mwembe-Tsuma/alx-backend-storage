#!/usr/bin/env python3
""" Main file """


import requests
import redis
from functools import wraps


def count_and_cache(func):
    @wraps(func)
    def wrapper(url):
        count_key = f"count:{url}"
        cache_key = f"cache:{url}"

        redis_client.incr(count_key)

        cached_result = redis_client.get(cache_key)
        if cached_result:
            return cached_result.decode('utf-8')

        result = func(url)
        redis_client.setex(cache_key, 10, result)

        return result
    return wrapper


@count_and_cache
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text
