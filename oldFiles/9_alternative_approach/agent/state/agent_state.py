from dataclasses import dataclass, field

@dataclass
class AgentState:
    user_request: str

    selected_tool: str | None = None
    tool_args: dict | None = None

    observations: list[str] = field(default_factory=list)

    final_answer: str | None = None

    iteration_count: int = 0
    max_iterations: int = 10

    finished: bool = False
