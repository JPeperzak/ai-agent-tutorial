from agent.prompts.generators import (
    generate_arguments_user_prompt,
    generate_user_prompt,
)

from agent.prompts.constants import (
    SYSTEM_PROMPT_GENERATE_PLAN,
    SYSTEM_PROMPT_DECIDE_ACTION,
    SYSTEM_PROMPT_CRITIC_ASSESSMENT,
    SYSTEM_PROMPT_FINAL_ANSWER,
    SYSTEM_PROMPT_SELECT_TOOL,
    SYSTEM_PROMPT_GENERATE_ARGUMENTS,
)

from agent.prompts.models import (
    CriticDecisionModel,
    FinalAnswerModel,
    SelectedToolModel
)

from agent.planner.models import (
    PlanModel,
    ActionSelectionModel
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
        user_prompt = generate_user_prompt(
            goal=self.goal, 
            observations_text=observations_text, 
            executed_actions_text=executed_actions_text, 
            tool_registry=self.tool_registry
        )
        decision = self.brain.think(
            system_prompt = SYSTEM_PROMPT_CRITIC_ASSESSMENT,
            user_prompt = user_prompt,
            temperature = 0.5,
            response_schema = CriticDecisionModel.model_json_schema(),
            think = False
        )
        validated_decision = CriticDecisionModel.model_validate_json(decision)
        self.memory.add_observation(f"Critic feedback: {validated_decision.reasoning}. Missing information: {validated_decision.missing_information}")
        return False if validated_decision.response.lower() == "more" else True

    def generate_final_answer(self) -> str:
        observations_text = self.memory.get_observations_text()
        user_prompt = generate_user_prompt(
            goal=self.goal, 
            observations_text=observations_text
        )
        decision = self.brain.think(
            system_prompt = SYSTEM_PROMPT_FINAL_ANSWER,
            user_prompt = user_prompt,
            temperature = 0.5,
            response_schema = FinalAnswerModel.model_json_schema(),
            think = False
        )
        validated_final_answer = FinalAnswerModel.model_validate_json(decision)
        return validated_final_answer.response

    def select_tool(self) -> str:
        observations_text = self.memory.get_observations_text()
        executed_actions_text = self.memory.get_executed_actions_text()
        # Looks very complicated, but really it just creates a string representation of a numbered list, listing the description of every step
        plan_text = "\n".join([f"{i}. {step.model_dump()["description"]}" for i, step in enumerate(self.memory.get_plan().steps, start=1)])
        user_prompt = generate_user_prompt(
            goal=self.goal, 
            observations_text=observations_text, 
            current_step_description=self.memory.get_current_step().description,
            plan_text=plan_text,
            executed_actions_text=executed_actions_text, 
            tool_registry=self.tool_registry
        )
        decision = self.brain.think(
            system_prompt = SYSTEM_PROMPT_SELECT_TOOL,
            user_prompt = user_prompt,
            temperature = 0.5,
            response_schema = SelectedToolModel.model_json_schema(),
            think = False
        )
        validated_selected_tool = SelectedToolModel.model_validate_json(decision)
        return validated_selected_tool.response

    def generate_arguments(self, selected_tool: str) -> Dict:
        observations_text = self.memory.get_observations_text()
        executed_actions_text = self.memory.get_executed_actions_text()
        plan_text = "\n".join([f"{i}. {step.model_dump()["description"]}" for i, step in enumerate(self.memory.get_plan().steps, start=1)])
        user_prompt = generate_arguments_user_prompt(
            self.goal, 
            self.memory.get_current_step().description,
            plan_text,
            observations_text, 
            executed_actions_text, 
            selected_tool, 
            self.tool_registry
        )
        response_model = self.tool_registry[selected_tool]["response_model"]
        decision = self.brain.think(
            system_prompt = SYSTEM_PROMPT_GENERATE_ARGUMENTS,
            user_prompt = user_prompt,
            temperature = 0.4,
            response_schema = response_model.model_json_schema(),
            think = False
        )

        validated_arguments = response_model.model_validate_json(decision).model_dump()
        return validated_arguments

    def create_plan(self) -> PlanModel:
        observations_text = self.memory.get_observations_text()
        user_prompt = generate_user_prompt(
            goal=self.goal, 
            observations_text=observations_text
        )
        decision = self.brain.think(
            system_prompt = SYSTEM_PROMPT_GENERATE_PLAN,
            user_prompt = user_prompt,
            temperature = 0.5,
            response_schema = PlanModel.model_json_schema(),
            think = False
        )
        validated_plan = PlanModel.model_validate_json(decision)
        return validated_plan

    def decide_action_for_current_step(self) -> str:
        # decide if another tool is needed, if the step is complete, or if the plan is done
        observations_text = self.memory.get_observations_text()
        plan_text = "\n".join([f"{i}. {step.model_dump()["description"]}" for i, step in enumerate(self.memory.get_plan().steps, start=1)])
        user_prompt = generate_user_prompt(
            goal=self.goal,
            observations_text=observations_text,
            current_step_description=self.memory.get_current_step().description,
            plan_text=plan_text,
            executed_actions_text=self.memory.get_executed_actions_text(),
            tool_registry=self.tool_registry
        )
        decision = self.brain.think(
            system_prompt=SYSTEM_PROMPT_DECIDE_ACTION,
            user_prompt=user_prompt,
            temperature=0.5,
            response_schema=ActionSelectionModel.model_json_schema(),
            think = False
        )
        validated_action = ActionSelectionModel.model_validate_json(decision)
        observation = f"""Action selected: '{validated_action.action}' 
Step: {self.memory.get_current_step().description}
Reason: {validated_action.reasoning}"""
        self.memory.add_observation(observation)
        return validated_action.action
        
        