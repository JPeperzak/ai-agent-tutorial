from agent.prompts.generators import (
    generate_select_action_user_prompt,
    generate_final_answer_user_prompt,
    generate_tool_selection_user_prompt,
    generate_arguments_user_prompt,
)

from agent.prompts.constants import (
    SYSTEM_PROMPT_SELECT_ACTION,
    SYSTEM_PROMPT_FINAL_ANSWER,
    SYSTEM_PROMPT_SELECT_TOOL,
    SYSTEM_PROMPT_GENERATE_ARGUMENTS,
)

from agent.prompts.schemas import (
    FinalAnswer,
    EnoughInformation,
    SelectedTool
)

from agent.brain import Brain
from typing import Dict, Any

class Executor:
    def __init__(
            self,
            brain: Brain, 
            tool_registry: Dict[str, Dict[str, Any]],
            goal: str
        ):
        self.goal = goal
        self.brain = brain
        self.tool_registry = tool_registry

    # Returns bool based on if the model has enough information to give a final answer
    def select_action(self, observations_text: str) -> bool:
        user_prompt = generate_select_action_user_prompt(self.goal, observations_text)
        decision = self.brain.think(
            system_prompt = SYSTEM_PROMPT_SELECT_ACTION,
            user_prompt = user_prompt,
            temperature = 0.2,
            json_schema = EnoughInformation.model_json_schema(),
            think = False
        )

        validated_decision = EnoughInformation.model_validate_json(decision)
        return True if validated_decision.response.lower() == "yes" else False

    def generate_final_answer(self, observations_text: str) -> str:
        user_prompt = generate_final_answer_user_prompt(self.goal, observations_text)
        decision = self.brain.think(
            system_prompt = SYSTEM_PROMPT_FINAL_ANSWER,
            user_prompt = user_prompt,
            temperature = 0.5,
            json_schema = FinalAnswer.model_json_schema(),
            think = False
        )

        validated_final_answer = FinalAnswer.model_validate_json(decision)
        return validated_final_answer.response

    def select_tool(self, observations_text: str) -> str:
        user_prompt = generate_tool_selection_user_prompt(self.goal, observations_text, self.tool_registry)
        decision = self.brain.think(
            system_prompt = SYSTEM_PROMPT_SELECT_TOOL,
            user_prompt = user_prompt,
            temperature = 0.5,
            json_schema = SelectedTool.model_json_schema(),
            think = False
        )

        validated_selected_tool = SelectedTool.model_validate_json(decision)
        return validated_selected_tool.response

    def generate_arguments(self, observations_text: str, selected_tool: str) -> Dict:
        user_prompt = generate_arguments_user_prompt(self.goal, observations_text, selected_tool, self.tool_registry)
        tool_schema = self.tool_registry[selected_tool]["json_schema"]
        decision = self.brain.think(
            system_prompt = SYSTEM_PROMPT_GENERATE_ARGUMENTS,
            user_prompt = user_prompt,
            temperature = 0.4,
            json_schema = tool_schema.model_json_schema(),
            think = False
        )

        validated_arguments = tool_schema.model_validate_json(decision).model_dump()
        return validated_arguments