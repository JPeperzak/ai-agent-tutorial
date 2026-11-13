from pathlib import Path

from agent.models.response import (
    PlanModel,
    PlanStepModel
)

from agent.models.data_types import (
    MemoryFact,
    ExecutedAction,
)

# The memory class has several storage lists:
#   - executed_actions is a list containing dictionaries structured {tool_name: {argument1: value1, argument2: value2, etc..}}
class Memory:
    def __init__(self):
        self.observations: list[str] = []
        self.executed_actions: list[ExecutedAction] = []
        self.plan: PlanModel = PlanModel(steps=[])
        self.facts: list[MemoryFact] = []
    
    def reset(self) -> None:
        self.observations = []
        self.executed_actions = []
        self.plan = PlanModel(steps=[])
        self.facts = []

    def add_observation(self, observation: str) -> None:
        self.observations.append(
            observation
        )

    def get_observations(
            self,
            last_k: int | None = None,
        ) -> list[str]:
        if last_k:
            index = last_k * -1
            return self.observations[index:]
        return self.observations

    def get_observations_text(
            self,
            last_k: int | None = None,
        ) -> str:
        return "\n\n".join(self.get_observations(last_k))

    def add_executed_actions(self, executed_action: ExecutedAction) -> None:
        self.executed_actions.append(executed_action)

    def get_executed_actions(self) -> list[ExecutedAction]:
        return self.executed_actions

    def get_executed_actions_text(self) -> str:
        return "\n".join(a.to_text() for a in self.executed_actions)

    def set_plan(self, plan: PlanModel) -> None:
        self.plan = plan

    def get_plan(self) -> PlanModel:
        return self.plan

    def get_current_step(self) -> PlanStepModel:        
        next_step = next((step for step in self.plan.steps if not step.completed), None)
        if next_step is None:
            raise RuntimeError("Expected an uncompleted plan step, but all steps are completed.")
        return next_step    

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
