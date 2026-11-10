import json
import re

from ollama import chat

from tools import (
    search_documents,
    read_document
)

from prompts import (
    AGENT_SYSTEM_PROMPT,
    generate_decide_next_step_user_prompt
)

TOOLS = {
    "search_documents": search_documents,
    "read_document": read_document
}

class Agent:
    def decide_next_step(self, question, scratchpad):
        observations = "\n".join(scratchpad)
        decide_next_step_user_prompt = generate_decide_next_step_user_prompt(question, observations)
        response = chat(
            model="qwen3.5:4b",
            messages=[
                {
                    "role": "system",
                    "content": AGENT_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": decide_next_step_user_prompt
                }
            ]
        )
        return response.message.content.strip()

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
                return "answer", {"response": formatted_decision["response"]}

            tool_name = formatted_decision["tool"]
            tool_function = TOOLS[tool_name]
            tool_arguments = dict(formatted_decision)
            tool_arguments.pop("tool")
            return "tool", {"tool_name": tool_name, "tool_function": tool_function, "tool_arguments": tool_arguments}
        except:
            return None, None

    def answer_question(self, question):
        scratchpad = []
        iterations = 0

        while True:
            decision = self.decide_next_step(question, scratchpad)
            decision_type, decision_content = self.format_decision(decision)
            if decision_type == None or decision_content == None:
                return f"ERROR FORMATTING DECISION\ndecision: {decision}"
            elif decision_type == "answer":
                return decision_content["response"]
            elif iterations == 8:
                return f"ERROR TOO MANY ITERATIONS\niterations: {iterations}"
                
            tool_function = decision_content["tool_function"]
            tool_arguments = decision_content["tool_arguments"]
            tool_name = decision_content["tool_name"]
            result = tool_function(**tool_arguments)
            scratchpad.append(f"Tool: {tool_name}")
            scratchpad.append(f"Tool arguments: {tool_arguments}")
            scratchpad.append(f"Result: {result}")
            iterations += 1