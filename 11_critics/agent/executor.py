from agent.prompts.generators import (
    generate_select_action_user_prompt,
    generate_final_answer_user_prompt,
    generate_tool_selection_user_prompt,
    generate_arguments_user_prompt,
)

from agent.prompts.constants import (
    SYSTEM_PROMPT_CRITIC_ASSESSMENT,
    SYSTEM_PROMPT_FINAL_ANSWER,
    SYSTEM_PROMPT_SELECT_TOOL,
    SYSTEM_PROMPT_GENERATE_ARGUMENTS,
)

from agent.prompts.schemas import (
    CriticDecision,
    FinalAnswer,
    SelectedTool
)

from agent.brain import Brain
from agent.memory import Memory
from typing import Dict, Any

class Executor:
    def __init__(
            self,
            brain: Brain, 
            memory: Memory,
            tool_registry: Dict[str, Dict[str, Any]],
            goal: str
        ):
        self.brain = brain
        self.memory = memory
        self.tool_registry = tool_registry
        self.goal = goal

    # Returns bool based on if the model has enough information to give a final answer
    def assess_information(self) -> bool:
        observations_text = self.memory.get_observations_text()
        executed_actions_text = self.memory.get_executed_actions_text()

        user_prompt = generate_select_action_user_prompt(self.goal, observations_text, executed_actions_text, self.tool_registry)
        decision = self.brain.think(
            system_prompt = SYSTEM_PROMPT_CRITIC_ASSESSMENT,
            user_prompt = user_prompt,
            temperature = 0.5,
            json_schema = CriticDecision.model_json_schema(),
            think = False
        )
        validated_decision = CriticDecision.model_validate_json(decision)
        self.memory.add_observation(f"Critic feedback: {validated_decision.reasoning}. Missing information: {validated_decision.missing_information}")
        print(f"critic's verdict: {validated_decision.response}")
        print(f"critic's reasoning: {validated_decision.reasoning}\n")
        return False if validated_decision.response.lower() == "more" else True

    def generate_final_answer(self) -> str:
        observations_text = self.memory.get_observations_text()
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

    def select_tool(self) -> str:
        observations_text = self.memory.get_observations_text()
        executed_actions_text = self.memory.get_executed_actions_text()
        user_prompt = generate_tool_selection_user_prompt(self.goal, observations_text, executed_actions_text, self.tool_registry)
        decision = self.brain.think(
            system_prompt = SYSTEM_PROMPT_SELECT_TOOL,
            user_prompt = user_prompt,
            temperature = 0.5,
            json_schema = SelectedTool.model_json_schema(),
            think = False
        )
        validated_selected_tool = SelectedTool.model_validate_json(decision)
        return validated_selected_tool.response

    def generate_arguments(self, selected_tool: str) -> Dict:
        observations_text = self.memory.get_observations_text()
        executed_actions_text = self.memory.get_executed_actions_text()
        user_prompt = generate_arguments_user_prompt(self.goal, observations_text, executed_actions_text, selected_tool, self.tool_registry)
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