from agent.constants.ActionTypeEnum import ActionType

class Planner:
    def decide_next_step(self, state):
        if state.final_answer:
            return ActionType.ANSWER

        if state.selected_tool is None:
            return ActionType.SELECT_TOOL

        if state.tool_args is None:
            return ActionType.GENERATE_ARGUMENTS

        return ActionType.EXECUTE_TOOL
