from typing import List, Dict
from pathlib import Path

from agent.models.response import (
    PlanModel,
    PlanStepModel
)

from agent.models.data_types import (
    MemoryFact
)

# The memory class has several storage lists:
#   - executed_actions is a list containing dictionaries structured {tool_name: {argument1: value1, argument2: value2, etc..}}
#   - observations contains all other observations. It might be useful to bring more structure to this.
class Memory:
    def __init__(self):
        self.observations: List[str] = []
        self.executed_actions: List[Dict[str, Dict]] = []
        self.plan: PlanModel | None = None
        self.facts: list[MemoryFact] = []

    def add_observation(self, observation: str) -> None:
        self.observations.append(
            observation
        )

    def get_observations(
            self,
            last_k: int | None = None,
        ) -> List[str]:
        if last_k:
            index = last_k * -1
            return self.observations[index:]
        return self.observations

    def get_observations_text(
            self,
            last_k: int | None = None,
        ) -> str:
        return "\n\n".join(self.get_observations(last_k))

    def add_executed_actions(self, executed_action: Dict[str, Dict]) -> None:
        self.executed_actions.append(executed_action)

    def get_executed_actions(self) -> List[Dict[str, Dict]]:
        return self.executed_actions

    def get_executed_actions_text(self) -> str:
        text = ""
        executed_actions = self.get_executed_actions()
        for tool in executed_actions:
            selected_tool, action_arguments = next(iter(tool.items()))
            text += (f"- {selected_tool}({", ".join(f"{key}={value}" for key, value in action_arguments.items())})\n")
        return text.rstrip()

    def set_plan(self, plan: PlanModel) -> None:
        self.plan = plan

    def get_plan(self) -> PlanModel | None:
        return self.plan

    def get_current_step(self) -> PlanStepModel | None:
        if not self.plan:
            return None
        
        for step in self.plan.steps:
            if not step.completed:
                return step

        return None

    def complete_current_step(self) -> None:
        current_step = self.get_current_step()

        if current_step:
            current_step.completed = True

    def add_facts(
            self,
            facts: list[MemoryFact],
    ) -> None:
        for fact in facts:
            if fact not in self.facts:
                self.facts.append(fact)

    def get_facts(self) -> list[MemoryFact]:
        return self.facts

    def log_memory(self):
        LOGS_DIR = Path(__file__).parent.parent / "logs"
        FILE_PATH = LOGS_DIR / "observations.txt"
        with open(FILE_PATH, "w", encoding="utf-8") as file:
            file.write(self.get_observations_text())
