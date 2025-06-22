import os
import pandas as pd
from pathlib import Path

from langchain_redis import RedisVectorStore

from src.services.embeddings_service import EmbeddingsService


class RedisVDBBuilder:
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
