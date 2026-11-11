from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        
    # Unsure how to type the output of this method
    def embed(self, text: str):
        return self.model.encode(text)