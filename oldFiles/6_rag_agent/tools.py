import os

def search_documents(query):
    matches = []

    for filename in os.listdir("knowledge"):

        with open(
            f"knowledge/{filename}",
            "r",
            encoding="utf-8"
        ) as file:
            content = file.read()
            if query.lower() in content.lower():
                matches.append(filename)

    return matches

def read_document(filename):
    with open(
        f"knowledge/{filename}",
        "r",
        encoding="utf-8"
    ) as file:
        return file.read()