from pydantic import BaseModel

class SearchDocuments(BaseModel):
    query: str
class ReadDocument(BaseModel):
    filename: str
class SemanticSearch(BaseModel):
    query: str