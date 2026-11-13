from tools.rag_tools import RetrieveKnowledgeTool
from tools.wikipedia_tools import SearchWikipediaTool
from tools.web_tools import SearchWebTool

from agent.models.tools import (
    RetrieveKnowledgeModel,
    SearchWikipediaModel,
    SearchWebModel,
)

from agent.models.data_types import (
    ToolRegistry,
    Tool,
)

from agent.data_processing.embedder import Embedder
from agent.data_processing.vector_store import VectorStore
from agent.data_processing.chunker import TextChunker


# When creating a new tool, make sure to create a BaseModel for it in tools.schemas.py
def build_tool_registry(
    embedder: Embedder,
    vector_store: VectorStore,
    chunker: TextChunker,
) -> ToolRegistry:
    tools = [
        Tool(
            name="retrieve_knowledge",
            description=(
                "Retrieve information from the local knowledge base using semantic search. "
                "Use this first whenever information is needed to answer a question."
            ),
            function=RetrieveKnowledgeTool(vector_store),
            args_model=RetrieveKnowledgeModel,
        ),
        Tool(
            name="search_wikipedia",
            description=(
                "Look up a Wikipedia article and return its most relevant passages. "
                "Use this when the local knowledge base lacks the needed information."
            ),
            function=SearchWikipediaTool(embedder, chunker),
            args_model=SearchWikipediaModel,
        ),
        Tool(
            name="search_web",
            description=(
                "Search the web for recent, niche or practical information (versions, how-tos, news). "
                "Use when the local knowledge base and Wikipedia did not help."
            ),
            function=SearchWebTool(embedder, chunker),
            args_model=SearchWebModel,
        ),
    ]
    # By turning the list into a dict rather than writing the dict out, you only have to type out every name once.
    #   This reduces the chance of errors due to typo's and thus ensures the key and name are the same.
    return {tool.name: tool for tool in tools}