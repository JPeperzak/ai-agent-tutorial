from pydantic import BaseModel
from typing import Literal

class EnoughInformation(BaseModel):
    response: Literal["yes", "no"]

class SelectedTool(BaseModel):
    response: Literal[    
        "list_files",
        "count_lines",
        "read_file",
        "search_documents",
        "read_document",
        "semantic_search"
    ]

class FinalAnswer(BaseModel):
    response: str

