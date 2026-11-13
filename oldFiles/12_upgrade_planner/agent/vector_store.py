# The VectorStore class is where we store the embedding values of the knowledge documents.
from sklearn.metrics.pairwise import cosine_similarity

from typing import Any, List, Dict

class VectorStore:
    def __init__(self):
        self.documents: List[Dict[str, Any]] = []

    def add_document(
        self,
        filename: str,
        content: str,
        embedding: Any
    ):
        self.documents.append({
            "filename": filename,
            "content": content,
            "embedding": embedding
        })

    def get_documents(self) -> List[Dict[str, Any]]:
        return self.documents

    def search(
        self,
        query_embedding: Any,
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []

        for document in self.documents:
            similarity = cosine_similarity(
                [query_embedding],
                [document["embedding"]]
            )[0][0]

            results.append({
                "filename": document["filename"],
                "content": document["content"],
                "similarity": similarity
            })

        results.sort(
            key=lambda result: result["similarity"],
            reverse=True
        )
        return results[:top_k]