from pathlib import Path

class KnowledgeLoader:
    def load_documents(
            self,
            knowledge_directory: str
    ) -> list[dict[str, str]]:
        documents = []
        for file_path in Path(knowledge_directory).iterdir():
            if file_path.is_file():
                with open(file_path, "r", encoding="utf-8") as file:
                    documents.append({
                        "filename": file_path.name,
                        "content": file.read()
                    })
        return documents