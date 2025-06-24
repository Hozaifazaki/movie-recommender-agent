from src.utils.data_utils import DataDownloader
from src.services.embeddings_service import EmbeddingsService
from src.db.redis_vdb_builder import RedisVDBBuilder
from src.services.cache_service import RedisCacheServices
from src.tools.retriver_tool import RetrieverTool

# Download data if needed
DataDownloader(save_data_dir="movie_recommendation_agent/src/data").download()

# Build vector database
embedding_service = EmbeddingsService()
vdb_builder = RedisVDBBuilder(data_path="movie_recommendation_agent/src/data/dataset",
                              file_name="movies.csv",
                              embedding_service=embedding_service)
vector_store = vdb_builder.build_vdb()

# Set up cache and chat history
redis_service = RedisCacheServices()
cache = redis_service.get_cache()
chat_history = redis_service.get_chat_history()

# Retrive something
tool = RetrieverTool(vector_store=vector_store, k=5)
result = tool.invoke({"query":"Toy Story"})

print(result)