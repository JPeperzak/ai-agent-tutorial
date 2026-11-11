from typing import List, Dict

# The memory class has several storage lists:
#   - executed_actions is a list containing dictionaries structured {tool_name: {argument1: value1, argument2: value2, etc..}}
#   - observations contains all other observations. It might be useful to bring more structure to this.
class Memory:
    def __init__(self):
        self.observations: List[str] = []
        self.executed_actions: List[Dict[str, Dict]] = []

    def add_observation(self, observation: str):
        self.observations.append(
            observation
        )

    def get_observations(self) -> List[str]:
        return self.observations

    def get_observations_text(self) -> str:
        return "\n".join(self.get_observations())

    def add_executed_actions(self, executed_action: Dict[str, Dict]):
        self.executed_actions.append(executed_action)

    def get_executed_actions(self) -> List[Dict[str, Dict]]:
        return self.executed_actions

    def get_executed_actions_text(self) -> str:
        text = ""
        executed_actions = self.get_executed_actions()
        for tool in executed_actions:
            selected_tool, action_arguments = next(iter(tool.items()))
            text += (f"- {selected_tool}({", ".join(f"{key}={value}" for key, value in action_arguments.items())})\n")
        return text
        