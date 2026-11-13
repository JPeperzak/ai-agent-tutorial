from agent.prompts.generators import (
    generate_arguments_user_prompt,
    generate_user_prompt,
    generate_facts_user_prompt,
)

from agent.prompts.constants import (
    SYSTEM_PROMPT_GENERATE_PLAN,
    SYSTEM_PROMPT_DECIDE_ACTION,
    SYSTEM_PROMPT_CRITIC_ASSESSMENT,
    SYSTEM_PROMPT_FINAL_ANSWER,
    SYSTEM_PROMPT_SELECT_TOOL,
    SYSTEM_PROMPT_GENERATE_ARGUMENTS,
)

from agent.models.response import (
    CriticDecisionModel,
    FinalAnswerModel,
)

from agent.models.response import (
    PlanModel,
    ActionSelectionModel,
    FactExtractionModel
)

from agent.brain import Brain
from agent.memory import Memory

from pydantic import create_model
from typing import Any, Literal

class Executor:
    def __init__(
            self,
            brain: Brain, 
            memory: Memory,
            tool_registry: dict[str, dict[str, Any]],
            goal: str
        ):
        self.brain = brain
        self.memory = memory
        self.tool_registry = tool_registry
        self.goal = goal

    # Returns bool based on if the model has enough information to give a final answer
    def assess_information(self) -> bool:
        executed_actions_text = self.memory.get_executed_actions_text()
        user_prompt = generate_user_prompt(
            goal=self.goal, 
            facts=self.memory.get_facts(),
            executed_actions_text=executed_actions_text, 
        )
        validated_decision = self.brain.think_structured(
            user_prompt = user_prompt,
            system_prompt = SYSTEM_PROMPT_CRITIC_ASSESSMENT,
            temperature = 0.5,
            response_model = CriticDecisionModel,
            think = False
        )
        self.memory.add_observation(f"Critic feedback: {validated_decision.reasoning}. Missing information: {validated_decision.missing_information}")
        return False if validated_decision.response.lower() == "more" else True

    def generate_final_answer(self) -> str:
        user_prompt = generate_user_prompt(
            goal=self.goal, 
            facts=self.memory.get_facts(),
        )
        validated_final_answer = self.brain.think_structured(
            user_prompt = user_prompt,
            system_prompt = SYSTEM_PROMPT_FINAL_ANSWER,
            temperature = 0.5,
            response_model = FinalAnswerModel,
            think = False
        )
        return validated_final_answer.response

    def select_tool(self) -> str:
        observations_text = self.memory.get_observations_text(3)
        executed_actions_text = self.memory.get_executed_actions_text()
        # Looks very complicated, but really it just creates a string representation of a numbered list, listing the description of every step
        plan_text = "\n".join([f"{i}. {step.model_dump()["description"]}" for i, step in enumerate(self.memory.get_plan().steps, start=1)])
        user_prompt = generate_user_prompt(
            goal=self.goal, 
            observations_text=observations_text, 
            facts=self.memory.get_facts(),
            current_step_description=self.memory.get_current_step().description,
            plan_text=plan_text,
            executed_actions_text=executed_actions_text, 
            tool_registry=self.tool_registry
        )
        tool_names = tuple(self.tool_registry.keys())
        SelectedToolModel = create_model("SelectedToolModel", response=(Literal[tool_names]))
        validated_selected_tool = self.brain.think_structured(
            user_prompt = user_prompt,
            system_prompt = SYSTEM_PROMPT_SELECT_TOOL,
            temperature = 0.5,
            response_model = SelectedToolModel,
            think = False
        )
        return validated_selected_tool.response

    def generate_arguments(self, selected_tool: str) -> dict:
        observations_text = self.memory.get_observations_text(3)
        executed_actions_text = self.memory.get_executed_actions_text()
        plan_text = "\n".join([f"{i}. {step.model_dump()["description"]}" for i, step in enumerate(self.memory.get_plan().steps, start=1)])
        user_prompt = generate_arguments_user_prompt(
            self.goal, 
            self.memory.get_current_step().description,
            plan_text,
            observations_text, 
            self.memory.get_facts(),
            executed_actions_text, 
            selected_tool, 
            self.tool_registry
        )
        response_model = self.tool_registry[selected_tool]["response_model"]
        validated_arguments = self.brain.think_structured(
            user_prompt = user_prompt,
            system_prompt = SYSTEM_PROMPT_GENERATE_ARGUMENTS,
            temperature = 0.4,
            response_model = response_model,
            think = False
        )
        return validated_arguments.model_dump()

    def create_plan(self) -> PlanModel:
        observations_text = self.memory.get_observations_text()
        user_prompt = generate_user_prompt(
            goal=self.goal, 
            observations_text=observations_text
        )
        validated_plan = self.brain.think_structured(
            user_prompt = user_prompt,
            system_prompt = SYSTEM_PROMPT_GENERATE_PLAN,
            temperature = 0.5,
            response_model = PlanModel,
            think = False
        )
        return validated_plan

    def decide_action_for_current_step(self) -> str:
        # decide if another tool is needed, if the step is complete, or if the plan is done
        observations_text = self.memory.get_observations_text(3)
        plan_text = "\n".join([f"{i}. {step.model_dump()["description"]}" for i, step in enumerate(self.memory.get_plan().steps, start=1)])
        user_prompt = generate_user_prompt(
            goal=self.goal,
            observations_text=observations_text,
            facts=self.memory.get_facts(),
            current_step_description=self.memory.get_current_step().description,
            plan_text=plan_text,
            executed_actions_text=self.memory.get_executed_actions_text(),
            tool_registry=self.tool_registry
        )
        validated_action = self.brain.think_structured(
            user_prompt=user_prompt,
            system_prompt=SYSTEM_PROMPT_DECIDE_ACTION,
            temperature=0.5,
            response_model=ActionSelectionModel,
            think = False
        )
        observation = f"""Action selected: '{validated_action.action}' 
Step: {self.memory.get_current_step().description}
Reason: {validated_action.reasoning}"""
        self.memory.add_observation(observation)
        return validated_action.action
        
    def extract_facts(
            self,
            retrieved_information: str
    ) -> dict[str, list[str]]:
        user_prompt = generate_facts_user_prompt(retrieved_information)
        validated_facts = self.brain.think_structured(
            user_prompt=user_prompt,
            temperature = 0.5,
            response_model = FactExtractionModel,
            think = False
        )
        facts_object = validated_facts.model_dump()
        return facts_object
