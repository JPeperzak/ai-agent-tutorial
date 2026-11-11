from pathlib import Path

from typing import List, Dict

class KnowledgeLoader:
    def load_documents(
            self,
            knowledge_directory: str
    ) -> List[Dict[str, str]]:
        documents = []
        for file_path in Path(knowledge_directory).iterdir():
            if file_path.is_file():
                with open(file_path, "r", encoding="utf-8") as file:
                    documents.append({
                        "filename": file_path.name,
                        "content": file.read()
                    })
        return documents