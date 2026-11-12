from tools.rag_tools import (
    search_documents,
    read_document,
    SemanticSearchTool
)

from tools.models import (
    SearchDocumentsModel,
    ReadDocumentModel,
    SemanticSearchModel
)

from agent.embedder import Embedder
from agent.vector_store import VectorStore

from typing import Any, Dict

# When creating a new tool, make sure to 
#   - Add its name to the SelectedTool BaseModel in prompts.schemas.py
#   - Create a BaseModel for it in tools.schemas.py
def build_tool_registry(
    embedder: Embedder,
    vector_store: VectorStore
) -> Dict[str, Dict[str, Any]]:
    semantic_search_tool = SemanticSearchTool(embedder, vector_store)
    return {
    "search_documents": {
        "function": search_documents,
        "description": (
            "Searches through the content of all knowledge documents "
            "and returns the filenames of all documents whose content "
            "includes at least one exact match with the query. Performs "
            "best when the query is a single word or phrase."
        ),
        "schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A search term or topic to look for knowledge about, such as 'refund policy', 'docker', or 'python'."
                }
            },
            "required": ["query"]
        },     
        "response_model": SearchDocumentsModel,      
    },
    "read_document": {
        "function": read_document,
        "description": (
            "Reads the contents of the knowledge document with the provided filename "
            "and returns its full text. ONLY use this when you are sure the filename exists."
        ),
        "schema": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Name of a file found with search_documents" #!!
                }
            },
            "required": ["filename"]
        },        
        "response_model": ReadDocumentModel,   
    },
    "semantic_search": {
        "function": semantic_search_tool,
        "description": (
            "Performs semantic similarity search across the knowledge base. "
            "Returns the most relevant content even when the query uses "
            "different wording than the document. Prefer this tool for "
            "retrieving information from documents."
        ),
        "schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A topic to look for information about."
                }
            },
            "required": ["query"]
        },     
        "response_model": SemanticSearchModel,      
    }
    }