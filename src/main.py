import os

from src.services.embeddings_service import EmbeddingsService
from src.services.redis_service import RedisService
from src.services.llm_service import LLMService

from src.crews.recommender_crew import RecommenderCrew

from src.utils.data_utils import DataDownloader
from src.utils.path_util import PathUtil
from src.utils.yaml_loader import read_yaml

def run():
    """Run the recommender crew."""
    # Initialize paths
    base_dir = os.getcwd() + "/src"
    PathUtil.initialize(base_dir)

    # VDB index name
    index_name = "movie_recommendations"


    # Connect to the vector database
    embedding_service = EmbeddingsService()
    redis_service = RedisService(data_path="./data/dataset",
                                file_name="movies.csv",
                                embedding_service=embedding_service,
                                vdb_name=index_name)
    
    redis_client = redis_service.get_redis_client()

    try: 
        if redis_client.ft(index_name).info():
            print(f"\n\n########## Using existing vector database index: {index_name} ##########\n\n")
            vector_store = redis_service.connect_to_existing_vdb()
    except Exception as e:
        print(f"\n\n########## Error checking index, creating new one: {str(e)} ##########\n\n")
        print(f"########## Creating new vector database index: {index_name }##########\n\n")
        # Download data if needed
        DataDownloader(save_data_dir="./data").download()
        vector_store = redis_service.build_vdb()
    
    # Set up cache and chat history
    cache = redis_service.get_cache()
    chat_history = redis_service.get_chat_history()

    # Intialize LLM
    model_config = read_yaml(PathUtil.get_config_file_path("llm_config.yaml"))
    llm = LLMService(model_config=model_config, selected_model="google_gemini")

    inputs = {'genre_preference': "I want a movie like Home alone but I do not like old movies, so I need it to be created after 2015"}
    # Create and run the crew
    result = RecommenderCrew(vector_store=vector_store, llm_service=llm).crew().kickoff(inputs=inputs)

    # Print the result
    print("\n\n=== FINAL REPORT ===\n\n")
    print(result.raw)
