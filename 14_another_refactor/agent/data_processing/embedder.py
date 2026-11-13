from sentence_transformers import SentenceTransformer

import numpy as np
from numpy.typing import NDArray

class Embedder:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        
    # Unsure how to type the output of this method
    def embed(self, text: str) -> NDArray[np.float32]:
        return self.model.encode(text)