from pydantic import BaseModel, Field


class RetrieverInput(BaseModel):
    query: str = Field(description="The search query for movies.")
