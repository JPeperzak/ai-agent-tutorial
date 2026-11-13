from tools.rag_tools import (
    RetrieveKnowledgeTool
)

from agent.models.tools import (
    RetrieveKnowledgeModel
)

from agent.data_processing.embedder import Embedder
from agent.data_processing.vector_store import VectorStore

from typing import Any, Dict

# When creating a new tool, make sure to 
#   - Add its name to the SelectedTool BaseModel in prompts.schemas.py
#   - Create a BaseModel for it in tools.schemas.py
def build_tool_registry(
    embedder: Embedder,
    vector_store: VectorStore
) -> Dict[str, Dict[str, Any]]:
    retrieve_knowledge = RetrieveKnowledgeTool(embedder, vector_store)
    return {
    "retrieve_knowledge": {
        "function": retrieve_knowledge,
        "description": (
                "Retrieve information from the local "
                "knowledge base using semantic search. "
                "Use this whenever information is needed "
                "to answer a question."
        ),
        "schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A topic to look for information about."
                },
                "top_k": {
                    "type": "int",
                    "description": "The tool will return the top_k amount of most similar content"
                }
            },
            "required": ["query"]
        },     
        "response_model": RetrieveKnowledgeModel,      
    }
    }