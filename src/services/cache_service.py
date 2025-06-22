import os

from langchain_redis import RedisCache, RedisChatMessageHistory


class RedisCacheServices:
    def __init__(self, session_id: str = "movie_recommendations"):
        self.session_id = session_id
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

    def get_cache(self):
        """Get a RedisCache instance.

        - Instantiates and returns a RedisCache object using the configured Redis URL.
        """
        return RedisCache(redis_url=self.redis_url)

    def get_chat_history(self):
        """Get a RedisChatMessageHistory instance for the current session.

        - Instantiates and returns a RedisChatMessageHistory object using the session ID and Redis URL.
        """
        return RedisChatMessageHistory(self.session_id, redis_url=self.redis_url)
