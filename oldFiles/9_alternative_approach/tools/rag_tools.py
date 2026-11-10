from pathlib import Path

KNOWLEDGE_DIR = Path(__file__).parent.parent / "knowledge"

def search_documents(query):
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

def read_document(filename):
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
        embedder,
        vector_store
    ): 
        self.vector_store = vector_store
        self.embedder = embedder

    # The __call__ method allows an instance of the class to be used as a function
    def __call__(self, query):
        query_embedding = self.embedder.embed(query)
        return self.vector_store.search(query_embedding)