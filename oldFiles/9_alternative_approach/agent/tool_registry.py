import json

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

def build_tool_registry(
    embedder,
    vector_store
):
    semantic_search_tool = SemanticSearchTool(embedder, vector_store)
    return {
    "list_files": {
        "function": list_files,
        "description": "Returns all project files that contain the agent's source code.",
        "schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    "count_lines": {
        "function": count_lines,
        "description": "Returns the number of lines in a file related to the agent's source code.",
        "schema": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Name of the file."
                }
            },
            "required": ["filename"]
        }
    },
    "read_file": {
        "function": read_file,
        "description": "Returns the full contents of a file related to the agent's source code.",
        "schema": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Name of the file."
                }
            },
            "required": ["filename"]
        }
    },
    "search_documents": {
        "function": search_documents,
        "description": (
            "Performs keyword-based document search. "
            "Use when you need exact word matches."
        ),
        "schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A search term or topic to look for, such as 'refund policy', 'docker', or 'python'."
                }
            },
            "required": ["query"]
        }
    },
    "read_document": {
        "function": read_document,
        "description": (
            "Reads the contents of a specific document and returns "
            "its full text. Use this after identifying a document "
            "with search_documents."
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
        }
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
        }
    }
    }