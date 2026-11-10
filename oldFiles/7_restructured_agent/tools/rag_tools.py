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