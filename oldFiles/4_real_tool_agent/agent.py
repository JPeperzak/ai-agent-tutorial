# The goal of this agent is that it should be able to answer the following questions by using the correct tool:
#   - What files are in the project?
#   - Show me the contents of agent.py
#   - How many python files exist?

import json
import re

from ollama import chat

from prompts import (
    TOOL_SELECTION_PROMPT,
    ANSWER_PROMPT,
    generate_user_answer_prompt
)

from tools import (
    list_files,
    read_file,
    count_lines
)

TOOLS = {
    "list_files": list_files,
    "read_file": read_file,
    "count_lines": count_lines
}

class Agent:
    def choose_tool(self, question):
        response = chat(
            model="qwen3.5:4b",
            messages=[
                {
                    "role": "system",
                    "content": TOOL_SELECTION_PROMPT
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )
        return response.message.content.strip()

    def generate_response(self, question, result):
        user_content = generate_user_answer_prompt(question, result)
        response = chat(
            model="qwen3.5:4b",
            messages=[
                {
                    "role": "system",
                    "content": ANSWER_PROMPT
                },
                {
                    "role": "user",
                    "content": user_content
                }
            ]
        )
        return response.message.content

    def format_tool_choice(self, tool_string):
        # Check tool_string for correct formatting and fix it if necessary
        if not tool_string.split()[0] == "{" or not tool_string.split()[-1] == "}":
            print("INCORRECT FORMAT DETECTED")
            print(f"Old format: {tool_string}")
            match = re.search(r"\{.*\}", tool_string, re.DOTALL)
            if match:
                tool_string = match.group()
                print(f"New format: {tool_string}")

        try:
            tool_request = json.loads(tool_string)
            tool_name = tool_request["tool"]
            tool_function = TOOLS[tool_name]
            tool_arguments = dict(tool_request)
            tool_arguments.pop("tool")
            return tool_function, tool_arguments
        except:
            return None, None
            
            

    def answer_question(self, question):
        tool_string = self.choose_tool(question)
        tool_function, tool_arguments = self.format_tool_choice(tool_string)
        if tool_function == None or tool_arguments == None:
            return f"ERROR FORMATTING TOOL CHOICE\ntool_string: {tool_string}"

        result = tool_function(**tool_arguments)
        return self.generate_response(question, result)
