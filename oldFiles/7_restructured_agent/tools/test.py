from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent / "agent"

def list_files():
    return [
        file.name
        for file in PROJECT_ROOT.iterdir()
    ]

result = list_files()
print(result)