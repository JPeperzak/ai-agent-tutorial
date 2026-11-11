from pydantic import BaseModel

class CountLines(BaseModel):
    filename: str
class ReadFile(BaseModel):
    filename: str
class SearchDocuments(BaseModel):
    query: str
class ReadDocument(BaseModel):
    filename: str
class SemanticSearch(BaseModel):
    query: str