from sentence_transformers import SentenceTransformer


class EmbeddingsService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts):
        """Embed a list of documents (text chunks).

        This method is required by LangChain RedisVectorStore.

        Args:
            texts (list of str): List of text documents to embed.

        Returns:
            list: List of embedding vectors, one per input text.
        """
        # For a list of documents
        return self.model.encode(texts, show_progress_bar=False).tolist()

    def embed_query(self, text):
        """Embed a single query string.

        This method is required by LangChain RedisVectorStore.

        Args:
            text (str): Query text to embed.

        Returns:
            list: Embedding vector for the query.
        """
        # For a single query string
        return self.model.encode([text], show_progress_bar=False)[0].tolist()
