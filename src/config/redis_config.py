from functools import cached_property
import os
import redis

class RedisConfig:
    def __init__(self):
        self.host = os.getenv("REDIS_HOST", "localhost")
        self.port = os.getenv("REDIS_PORT", "6379")
        self.db = os.getenv("REDIS_DB", "0")
        self.decode_responses = True

    @cached_property
    def get_client(self):
        """Returns a cached Redis client instance."""
        return redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            decode_responses=self.decode_responses,
        )
