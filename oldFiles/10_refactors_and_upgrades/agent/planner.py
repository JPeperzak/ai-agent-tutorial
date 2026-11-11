from agent.executor import Executor
from agent.brain import Brain

from typing import Any, Dict, List

class Planner:
    def decide_next_step(
        self,
        executor: Executor,
        observations: List[str],
        tool_registry: Dict[str, Dict[str, Any]],
    ):
        observations_text = "\n".join(
            observations
        )

        # Select an action based on available information (observations)
        try:
            enough_information = executor.select_action(observations_text)
        except BaseException as e:
            return {"action": "error", "response": f"ERROR SELECTING ACTION\n{str(e)}"}

        # If there is enough information, generate the final answer
        if enough_information:
            try:
                final_answer = executor.generate_final_answer(observations_text)
                return {"action": "answer", "response": final_answer}
            except BaseException as e:
                return {"action": "error", "response": f"ERROR GENERATING FINAL ANSWER\n{str(e)}"}
            
        # If more information is required, select a tool to obtain it
        try:
            selected_tool = executor.select_tool(observations_text)
        except BaseException as e:
            return {"action": "error", "response": f"ERROR SELECTING TOOL\n{str(e)}"}

        # If the selected tool requires arguments, generate them
        try:
            if len(tool_registry[selected_tool]["schema"]["properties"]) > 0:
                validated_arguments = executor.generate_arguments(observations_text, selected_tool)
            else:
                validated_arguments = {}
            return {"action": "tool", "selected_tool": selected_tool, "arguments": validated_arguments}
        except BaseException as e:
            return {"action": "error", "response": f"ERROR SELECTING TOOL\n{str(e)}"}