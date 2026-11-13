from pydantic import BaseModel

class MemoryFact(BaseModel):
    statement: str
    source: str
    confidence: float = 1.0

class RetrievedPassage(BaseModel):
    source: str     # a filename or URL
    content: str

class ToolResult(BaseModel):
    passages: list[RetrievedPassage] = []
    message: str = ""       # explanation when there are no passages (no results, errors)

    def has_results(self) -> bool:
        return len(self.passages) > 0

    # Note that this will now be the only place where results are turned into text for the LLM
    def to_text(self) -> str:
        if not self.passages:
            return self.message or "The tool returned no results."
        blocks = [
            f"RESULT {i}:\nSource: {p.source}\nContent: {p.content}"
            for i, p in enumerate(self.passages, start=1)
        ]
        return "\n\n".join(blocks)