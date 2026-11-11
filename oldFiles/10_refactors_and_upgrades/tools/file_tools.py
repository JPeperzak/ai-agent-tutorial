from pathlib import Path

AGENT_DIR = Path(__file__).parent.parent / "agent"

def list_files() -> str:
    return [
        file.name
        for file in AGENT_DIR.iterdir()
    ]
def count_lines(filename: str) -> int:
    file_path = AGENT_DIR / filename
    with open(file_path, "r", encoding="utf-8") as file:
        return len(file.readlines())

def read_file(filename: str) -> str:
    file_path = AGENT_DIR / filename
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()