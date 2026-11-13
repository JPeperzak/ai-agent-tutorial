from tools.rag_tools import RetrieveKnowledgeTool
from tools.wikipedia_tools import SearchWikipediaTool
from tools.web_tools import SearchWebTool

from agent.models.tools import (
    RetrieveKnowledgeModel,
    SearchWikipediaModel,
    SearchWebModel,
)

from agent.data_processing.embedder import Embedder
from agent.data_processing.vector_store import VectorStore
from agent.data_processing.chunker import TextChunker

from typing import Any

# When creating a new tool, make sure to create a BaseModel for it in tools.schemas.py
def build_tool_registry(
    embedder: Embedder,
    vector_store: VectorStore,
    chunker: TextChunker,
) -> dict[str, dict[str, Any]]:
    # Notice how we can actually generate the schema using the model when we add 
    #   description fields to the attributes in the model definition.
    return {
        "retrieve_knowledge": {
            "function": RetrieveKnowledgeTool(vector_store),
            "description": (
                    "Retrieve information from the local "
                    "knowledge base using semantic search. "
                    "Use this first whenever information is needed "
                    "to answer a question."
            ),
            "schema": RetrieveKnowledgeModel.model_json_schema(),     
            "response_model": RetrieveKnowledgeModel,      
        },
        "search_wikipedia": {
            "function": SearchWikipediaTool(embedder, chunker),
            "description": (
                "Look up a Wikipedia article and return its most relevant passages. "
                "Use this when the local knowledge base lacks the needed information."
            ),
            "schema": SearchWikipediaModel.model_json_schema(),
            "response_model": SearchWikipediaModel,
        },
        "search_web": {
            "function": SearchWebTool(embedder, chunker),
            "description": "Search the web for recent, niche or practical information (versions, how-tos, news). Use when the local knowledge base and Wikipedia did not help.",
            "schema": SearchWebModel.model_json_schema(),
            "response_model": SearchWebModel,
        }
    }