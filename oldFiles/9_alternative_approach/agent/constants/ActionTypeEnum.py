from enum import Enum

class ActionType(Enum):
    SELECT_TOOL = "select_tool"
    GENERATE_ARGUMENTS = "generate_arguments"
    EXECUTE_TOOL = "execute_tool"
    ANSWER = "answer"