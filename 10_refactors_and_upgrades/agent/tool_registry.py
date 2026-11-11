from tools.file_tools import (
    list_files,
    count_lines,
    read_file
)

from tools.rag_tools import (
    search_documents,
    read_document,
    SemanticSearchTool
)

from tools.schemas import (
    CountLines,
    ReadFile,
    SearchDocuments,
    ReadDocument,
    SemanticSearch
)

from agent.embedder import Embedder
from agent.vector_store import VectorStore

from typing import Any, Dict

# When creating a new tool, make sure to add its name to the SelectedTool BaseModel in prompts.schemas.py
def build_tool_registry(
    embedder: Embedder,
    vector_store: VectorStore
) -> Dict[str, Dict[str, Any]]:
    semantic_search_tool = SemanticSearchTool(embedder, vector_store)
    return {
    "list_files": {
        "function": list_files,
        "description": "Returns all project files containing the agent's source code. Do not use this to gain knowledge.",
        "schema": {
            "type": "object",
            "properties": {},
            "required": []
        },
        "json_schema": None,        
    },
    "count_lines": {
        "function": count_lines,
        "description": (
            "Returns the number of lines in a file containing the agent's source code."
            "Use this after identifying valid filenames with list_files."
        ),
        "schema": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Name of the file."
                }
            },
            "required": ["filename"]
        },
        "json_schema": CountLines,           
    },
    "read_file": {
        "function": read_file,
        "description": (
            "Returns the full contents of a file containing the agent's source code."
            "Use this after identifying valid filenames with list_files."
        ),
        "schema": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Name of the file."
                }
            },
            "required": ["filename"]
        },
        "json_schema": ReadFile,           
    },
    "search_documents": {
        "function": search_documents,
        "description": (
            "Searches through the content of all knowledge documents "
            "and returns the filenames of all documents whose content "
            "includes at least one exact match with the query. "
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
        "json_schema": SearchDocuments,      
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
        "json_schema": ReadDocument,   
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
                    "description": "A natural language query."
                }
            },
            "required": ["query"]
        },     
        "json_schema": SemanticSearch,      
    }
    }