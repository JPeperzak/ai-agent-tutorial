from pathlib import Path
from typing import List

from agent.embedder import Embedder
from agent.vector_store import VectorStore

KNOWLEDGE_DIR = Path(__file__).parent.parent / "knowledge"

def search_documents(query: str) -> List[str]:
    matches = []

    for filename in [file.name for file in KNOWLEDGE_DIR.iterdir()]:
        file_path = KNOWLEDGE_DIR / filename
        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:
            content = file.read()
            if query.lower() in content.lower():
                matches.append(filename)

    return matches

def read_document(filename: str) -> str:
    file_path = KNOWLEDGE_DIR / filename
    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:
        return file.read()

class SemanticSearchTool:
    def __init__(
        self,
        embedder: Embedder,
        vector_store: VectorStore
    ): 
        self.vector_store = vector_store
        self.embedder = embedder

    # The __call__ method allows an instance of the class to be used as a function
    def __call__(self, query: str):
        query_embedding = self.embedder.embed(query)
        return self.vector_store.search(query_embedding)