#!/usr/bin/env python3
"""
Using Redis NoSQL database
"""

import redis
import uuid
from typing import Any, Callable, Union

class Cache:
    """
    Initializes an Object for data
    """

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        """

        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key



