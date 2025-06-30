import os
import pandas as pd
from pathlib import Path
import redis

from langchain_redis import RedisVectorStore, RedisCache, RedisChatMessageHistory

from src.services.embeddings_service import EmbeddingsService


class RedisService:
    def __init__(self, data_path: str,
                 file_name: str,
                 embedding_service: EmbeddingsService,
                 vdb_name: str = "movie_recommendations"):
        self.data_path = Path(data_path)
        self.file_name = file_name
        self.embedding_service = embedding_service
        self.vdb_name = vdb_name
        self.file_name = file_name
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self._client = None

    def get_redis_client(self):
        """Get a Redis client connection.
        
        - Lazily instantiates and returns a Redis client using the configured Redis URL.
        """
        if self._client is None:
            self._client = redis.from_url(self.redis_url)
        return self._client
    
    def get_cache(self):
        """Get a RedisCache instance.

        - Instantiates and returns a RedisCache object using the configured Redis URL.
        """
        return RedisCache(redis_url=self.redis_url)

    def get_chat_history(self):
        """Get a RedisChatMessageHistory instance for the current session.

        - Instantiates and returns a RedisChatMessageHistory object using the vdb name and Redis URL.
        """
        return RedisChatMessageHistory(self.vdb_name, redis_url=self.redis_url)

    def build_vdb(self):
        """Build the Redis vector database from the provided CSV file.

        - Reads the CSV file into a DataFrame.
        - Creates a RedisVectorStore from the text and metadata.
        - Returns the created vector store instance.
        """
        df = pd.read_csv(self.data_path / self.file_name)
        vector_store = RedisVectorStore.from_texts(
            texts=df['title'].tolist(),
            metadatas=df.to_dict('records'),
            embedding=self.embedding_service,
            redis_url=self.redis_url,
            index_name=self.vdb_name
        )
        return vector_store
    
    def connect_to_existing_vdb(self):
        """Connect to an existing vector database without rebuilding it.
        
        - Creates a connection to an existing Redis vector store.
        - Returns the connected vector store instance.
        """
        return RedisVectorStore.from_existing_index(
            embedding=self.embedding_service,
            index_name=self.vdb_name,
            redis_url=self.redis_url
        )