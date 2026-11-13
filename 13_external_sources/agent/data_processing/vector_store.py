# The VectorStore class is where we store the embedding values of the knowledge documents.
from sklearn.metrics.pairwise import cosine_similarity
from numpy.typing import NDArray
import numpy as np

from typing import Any, List, Dict

from agent.models.data_processing import (
    VectorEntryModel, 
    DocumentChunkModel,
)

class VectorStore:
    def __init__(self):
        self.entries: List[VectorEntryModel] = []

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
        query_embedding: NDArray[np.float32],
        top_k: int = 5
    ) -> str:
        results: List[Dict[str, Any]] = []

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
        content = results[:top_k]
        content_formatted = [f"RESULT {i}:\nFile: {result["filename"]}\nChunk: {result["chunk_index"]}\nContent: {result["content"]}" for i, result in enumerate(content, start=1)]
        return "--- start of retrieve_knowledge results ---\n" + "\n\n".join(content_formatted) + "\n--- end of retrieve_knowledge results ---"