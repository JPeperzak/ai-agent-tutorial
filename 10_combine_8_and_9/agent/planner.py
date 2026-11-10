import json
import re

from agent.prompts import (
    AGENT_SYSTEM_PROMPT,
    generate_user_prompt
)

from agent.tool_registry import build_tool_prompt

class Planner:
    def __init__(self, brain):
        self.brain = brain

    def decide_next_step(
        self,
        goal,
        observations,
        tools
    ):
        observations_text = "\n".join(
            observations
        )

        tool_descriptions = build_tool_prompt(tools)

        user_prompt = generate_user_prompt(goal, observations_text, tool_descriptions)
        decision = self.brain.think(
            AGENT_SYSTEM_PROMPT,
            user_prompt
        )

        print("\nPLANNER DECISION:")
        print(decision)

        return self.format_decision(decision)

    def format_decision(self, decision):
        # Check tool_string for correct formatting and fix it if necessary
        if not decision.split()[0] == "{" or not decision.split()[-1] == "}":
            print("INCORRECT FORMAT DETECTED")
            print(f"Old format: {decision}")
            match = re.search(r"\{.*\}", decision, re.DOTALL)
            if match:
                decision = match.group()
                print(f"New format: {decision}")

        try:
            formatted_decision = json.loads(decision)
            if formatted_decision.get("action") == "answer":
                return {"type": "answer", "response": formatted_decision["response"]}
            if formatted_decision.get("arguments"):
                formatted_decision.update(formatted_decision.pop("arguments"))
            
            tool_name = formatted_decision["tool"]
            tool_arguments = dict(formatted_decision)
            tool_arguments.pop("tool")
            return {"type": "tool", "tool_name": tool_name, "tool_arguments": tool_arguments}
        except:
            return {"type": "error", "response": f"ERROR FORMATTING DECISION\ndecision: {decision}"}