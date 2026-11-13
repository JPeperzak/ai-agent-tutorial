from pydantic import BaseModel
from typing import List

# Each chunk represents a retrievable piece of information, a subset of content from a document
class DocumentChunkModel(BaseModel):
    filename: str
    chunk_index: int
    content: str

class VectorEntryModel(DocumentChunkModel):
    # We use a list instead of a NDArray[np.float32] because numpy arrays
    # are not serializable to JSON whereas lists are.
    embedding: List[float]