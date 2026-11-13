from pydantic import BaseModel
from typing import Any
from collections.abc import Callable
from dataclasses import dataclass

class MemoryFact(BaseModel):
    statement: str
    source: str
    confidence: float = 1.0

class RetrievedPassage(BaseModel):
    source: str     # a filename or URL
    content: str

class ToolCall(BaseModel):
    tool_name: str
    arguments: dict[str, Any]

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

class ExecutedAction(ToolCall):

    def to_text(self) -> str:
        args = ", ".join(f"{k}={v}" for k, v in self.arguments.items())
        return f"- {self.tool_name}({args})"

class Document(BaseModel):
    file_name: str
    content: str

# The dataclass tag writes out the __init__ for you.
# Setting frozen to True means that you cannot change attribute values of an object after it is created
@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    # Callable[..., ToolResult] means anything you can call like a function (Callable), with any arguments (...), that returns a ToolResult (ToolResult)
    function: Callable[..., ToolResult]
    args_model: type[BaseModel]

    # @property means that it computes the JSON schema each time you access tool.schema (no parentheses). This replaces the stored "schema" entry. Since the schema is always derived from the model, storing both meant two copies that could drift apart. Now there’s only one source of truth.
    @property
    def schema(self) -> dict[str, Any]:
        return self.args_model.model_json_schema()

ToolRegistry = dict[str, Tool]