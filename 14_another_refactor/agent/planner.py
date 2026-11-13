from agent.executor import Executor
from agent.memory import Memory
from agent.models.response import Action
from agent.models.data_types import (
    ExecutedAction,
    ToolRegistry,
    ToolCall,
)

class Planner:
    def __init__(self, memory: Memory):
        self.memory = memory

    def ensure_plan_exists(
        self,
        executor: Executor     
    ) -> None:
        current_plan = self.memory.get_plan()
        if current_plan.steps:
            return

        plan = executor.create_plan()
        self.memory.set_plan(plan)

    def decide_next_action(
            self,
            executor: Executor,
    ) -> Action:
        self.ensure_plan_exists(executor)
        current_plan = self.memory.get_plan()

        if not any(step.completed == False for step in current_plan.steps):
            observation = f"""
Action 'done' selected.
Reason: All steps are completed.
"""
            self.memory.add_observation(observation)
            return Action.DONE

        return executor.decide_action_for_current_step()

    def decide_tool(
        self,
        executor: Executor,
        tool_registry: ToolRegistry,     
    ) -> ToolCall:
        selected_tool = executor.select_tool()

        # If the selected tool requires arguments, generate them
        if tool_registry[selected_tool].args_model.model_fields:
            validated_arguments = executor.generate_arguments(selected_tool)
            self.memory.add_executed_actions(ExecutedAction(tool_name=selected_tool, arguments=validated_arguments))
        else:
            validated_arguments = {}
        return ToolCall(tool_name=selected_tool, arguments=validated_arguments)