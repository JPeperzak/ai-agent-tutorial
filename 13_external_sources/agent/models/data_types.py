from pydantic import BaseModel

class MemoryFact(BaseModel):
    statement: str
    source: str
    confidence: float = 1.0