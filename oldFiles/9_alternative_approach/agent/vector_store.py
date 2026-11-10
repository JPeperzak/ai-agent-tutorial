from sklearn.metrics.pairwise import cosine_similarity

class VectorStore:
    def __init__(self):
        self.documents = []

    def add_document(
        self,
        filename,
        content,
        embedding
    ):
        self.documents.append({
            "filename": filename,
            "content": content,
            "embedding": embedding
        })

    def get_documents(self):
        return self.documents

    def search(
        self,
        query_embedding,
        top_k=3
    ):
        results = []

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