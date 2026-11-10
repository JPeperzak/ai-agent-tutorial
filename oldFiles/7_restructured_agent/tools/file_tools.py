from pathlib import Path

AGENT_DIR = Path(__file__).parent.parent / "agent"

def list_files():
    return [
        file.name
        for file in AGENT_DIR.iterdir()
    ]
def count_lines(filename):
    file_path = AGENT_DIR / filename
    with open(file_path, "r", encoding="utf-8") as file:
        return len(file.readlines())

def read_file(filename):
    file_path = AGENT_DIR / filename
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()