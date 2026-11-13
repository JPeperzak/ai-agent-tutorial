from agent.data_processing.chunker import TextChunker
from agent.data_processing.embedder import Embedder
from agent.data_processing.vector_store import VectorStore
from agent.models.data_types import RetrievedPassage

# This class can be used as a temporary storage to generate chunks, embed some texts, ask one question, and then discard.
class TemporaryIndex:
    def __init__(
            self,
            embedder: Embedder,
            chunker: TextChunker,
    ):
        self.embedder = embedder
        self.chunker = chunker
        self.store = VectorStore(self.embedder)

    def add_text(
            self,
            source_name: str,
            text: str,
    ) -> None:
        for chunk in self.chunker.chunk_document(source_name, text):
            self.store.add(chunk, self.embedder.embed(chunk.content))

    def search(
            self,
            query: str,
            top_k: int = 5,
    ) -> list[RetrievedPassage]:
        return self.store.search(query, top_k)