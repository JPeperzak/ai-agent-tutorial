from agent.data_processing.vector_store import VectorStore

from agent.models.data_types import ToolResult

class RetrieveKnowledgeTool:
    def __init__(
        self,
        vector_store: VectorStore
    ): 
        self.vector_store = vector_store

    # The __call__ method allows an instance of the class to be used as a function
    def __call__(self, query: str, top_k: int = 5) -> ToolResult:
        passages = self.vector_store.search(query, top_k)
        if not passages:
            return ToolResult(message=f"No relevant information found in the local knowledge base for '{query}'.")
        return ToolResult(passages=passages)