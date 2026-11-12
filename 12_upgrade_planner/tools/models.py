from pydantic import BaseModel

class SearchDocumentsModel(BaseModel):
    query: str
class ReadDocumentModel(BaseModel):
    filename: str
class SemanticSearchModel(BaseModel):
    query: str