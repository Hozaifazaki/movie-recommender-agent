from pydantic import PrivateAttr, BaseModel
from typing import Type

from crewai.tools import BaseTool

from src.data_models.retriver_input import RetrieverInput


class RetrieverTool(BaseTool):
    name: str = "Movie Database Lookup"
    description: str = "Search for movies in the database based on titles or descriptions."
    args_schema: Type[BaseModel] = RetrieverInput
    return_direct: bool = True

    _vector_store: object = PrivateAttr()
    _k: int = PrivateAttr(default=5)

    def __init__(self, vector_store, k: int = 5, **kwargs):
        super().__init__(**kwargs)
        self._vector_store = vector_store
        self._k = k

    def _run(self, query: str) -> str:
        """Synchronous search implementation."""
        results = self._vector_store.similarity_search(query, k=self._k)
        return "\n".join(f"{i+1}. {doc.page_content}" for i, doc in enumerate(results))
