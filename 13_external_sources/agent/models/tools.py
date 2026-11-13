from pydantic import BaseModel

class RetrieveKnowledgeModel(BaseModel):
    query: str