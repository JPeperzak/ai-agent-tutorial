from pathlib import Path
from agent.models.data_types import Document

class KnowledgeLoader:
    def load_documents(
            self,
            knowledge_directory: str
    ) -> list[Document]:
        documents = []
        for file_path in Path(knowledge_directory).iterdir():
            if file_path.is_file():
                with open(file_path, "r", encoding="utf-8") as file:
                    documents.append(Document(file_name=file_path.name, content=file.read()))
        return documents