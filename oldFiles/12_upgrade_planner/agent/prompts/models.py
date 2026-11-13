from pydantic import BaseModel
from typing import Literal

class CriticDecisionModel(BaseModel):
    response: Literal["enough", "more", "exhausted"]
    reasoning: str
    missing_information: str

class SelectedToolModel(BaseModel):
    response: Literal[    
        "search_documents",
        "read_document",
        "semantic_search"
    ]

class FinalAnswerModel(BaseModel):
    response: str

