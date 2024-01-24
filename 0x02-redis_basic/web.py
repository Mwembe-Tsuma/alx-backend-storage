#!/usr/bin/env python3
"""Main file"""


import redis
import requests
from functools import wraps
from typing import Callable


def track_get_page(fn: Callable) -> Callable:
    """ Implementing an expiring web cache and tracker """
    @wraps(fn)
    def wrapper(url: str) -> str:
        redis_client = redis.Redis()
        count_key = f'count:{url}'
        cache_key = f'cache:{url}'

        redis_client.incr(count_key)
        cached_page = redis_client.get(cache_key)
        if cached_page:
            return cached_page.decode('utf-8')

        response = fn(url)
        redis_client.setex(cache_key, 10, response)
        return response
    return wrapper


@track_get_page
def get_page(url: str) -> str:
    """Makes a http request to a given endpoint"""
    response = requests.get(url)
    return response.text
