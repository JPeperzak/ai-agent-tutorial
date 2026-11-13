# The VectorStore class is where we store the embedding values of the knowledge documents.
from sklearn.metrics.pairwise import cosine_similarity
from numpy.typing import NDArray
import numpy as np

from agent.data_processing.embedder import Embedder

from agent.models.data_processing import (
    VectorEntryModel, 
    DocumentChunkModel,
)

from agent.models.data_types import RetrievedPassage

class VectorStore:
    def __init__(self, embedder: Embedder):
        self.embedder = embedder
        self.entries: list[VectorEntryModel] = []

    # I think it's possible to rewrite this so that embedding is no longer
    # a required parameter, now that we pass embedder in the constructor we should be able to make our own embedding.
    def add(
            self,
            chunk: DocumentChunkModel,
            embedding: NDArray[np.float32],
    ) -> None:
        chunk_object = chunk.model_dump()
        self.entries.append(VectorEntryModel(
            filename=chunk_object["filename"],
            chunk_index=chunk_object["chunk_index"],
            content=chunk_object["content"],
            embedding=embedding.tolist(),
            )
        )

    def search(
        self,
        query: str,
        top_k: int = 5,
        min_similarity: float = 0.25,           # TO DO: Run a few test queries and see where relevant and irrelevant chunks fall for your embedded model, then adjust the value.
    ) -> list[RetrievedPassage]:
        results = []
        query_embedding = self.embedder.embed(query)

        for vector_entry in self.entries:
            vector_entry_object = vector_entry.model_dump()
            similarity = cosine_similarity(
                [query_embedding],
                [vector_entry_object["embedding"]]
            )[0][0]

            results.append({
                "similarity": similarity,
                "filename": vector_entry_object["filename"],
                "chunk_index": vector_entry_object["chunk_index"],
                "content": vector_entry_object["content"]
            })

        results.sort(
            key=lambda result: result["similarity"],
            reverse=True
        )
        return [
            RetrievedPassage(source=r["filename"], content=r["content"])
            for r in results[:top_k]
            if r["similarity"] >= min_similarity
        ]