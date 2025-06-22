import time

from langchain_redis import RedisVectorStore

from src.services.embeddings_service import EmbeddingsService

def main():
    # Initialize embedding service
    embedding_service = EmbeddingsService()

    # Connect to existing Redis vector store
    vector_store = RedisVectorStore.from_existing_index(
        index_name="movie_recommendations",
        embedding=embedding_service,
        redis_url="redis://localhost:6379"  # Adjust if needed
    )

    # Query the vector store and measure time
    query = "Toy Story"
    print(f"Testing similarity search for: '{query}'")
    start = time.time()
    results = vector_store.similarity_search(query, k=3)
    elapsed = time.time() - start
    for i, doc in enumerate(results, 1):
        print(f"{i}. {doc.page_content} | Metadata: {doc.metadata}")
    print(f"\nSearch time: {elapsed:.4f} seconds")

    # Optional: similarity search with score
    print("\nTesting similarity search with score:")
    start = time.time()
    results_with_scores = vector_store.similarity_search_with_score(query, k=3)
    elapsed = time.time() - start
    for i, (doc, score) in enumerate(results_with_scores, 1):
        print(f"{i}. {doc.page_content} | Score: {score:.3f}")
    print(f"\nSearch with score time: {elapsed:.4f} seconds")

if __name__ == "__main__":
    main()
