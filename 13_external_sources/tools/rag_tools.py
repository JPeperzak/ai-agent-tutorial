from agent.data_processing.embedder import Embedder
from agent.data_processing.vector_store import VectorStore

class RetrieveKnowledgeTool:
    def __init__(
        self,
        embedder: Embedder,
        vector_store: VectorStore
    ): 
        self.vector_store = vector_store
        self.embedder = embedder

    # The __call__ method allows an instance of the class to be used as a function
    def __call__(self, query: str, top_k: int = 5) -> str:
        query_embedding = self.embedder.embed(query)
        return self.vector_store.search(query_embedding, top_k)