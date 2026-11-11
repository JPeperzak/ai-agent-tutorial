from pydantic import BaseModel
from typing import Literal

class CriticDecision(BaseModel):
    response: Literal["enough", "more", "exhausted"]
    reasoning: str
    missing_information: str

class SelectedTool(BaseModel):
    response: Literal[    
        "search_documents",
        "read_document",
        "semantic_search"
    ]

class FinalAnswer(BaseModel):
    response: str

