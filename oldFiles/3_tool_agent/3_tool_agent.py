import time
import json
import re
from ollama import chat

from tools import (
    get_temperature,
    get_age_category
)

TOOLS = {
    "temperature": get_temperature,
    "age": get_age_category
}

class Tool_Agent:
    def __init__(self):
        self.memory = []

    def choose_tool(self, question):
        response = chat(
            model="qwen3.5:4b",
            messages=[
                {
                    "role": "system",
                    "content": """
                        Available tools, formatted toolname(inputData, datatype) :

                        temperature(location, string)
                        age(age, int)

                        Respond to the question with ONLY a JSON object of format:
                        {
                            "tool": "toolname",
                            "inputDataValue": "value"
                        }

                        Here are some examples:
                        - Question: 
                        "What is the weather like in Berlin?"
                        - Answer: 
                        {
                            "tool": "temperature",
                            "inputDataValue": "Berlin"
                        }

                        - Question:
                        "Would you consider 38 to be old?"
                        - Answer:
                        {
                            "tool": "age",
                            "inputDataValue": 38
                        }
                    """
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )
        return response.message.content.strip().lower()

    def generate_response(self, question, result):
        response = chat(
            model="qwen3.5:4b",
            messages=[
                {
                    "role": "system",
                    "content": """
Answer the user's question using the provided tool result.
Do not use Markdown syntax in your response.
Do not mention the tool in your response.
"""
                },
                {
                    "role": "user",
                    "content": f"""
Question:
{question}

Tool Result:
{result}
"""
                }
            ]
        )
        return response.message.content
    
    def answer_question(self, question):
        start = time.time()
        tool_string = self.choose_tool(question)
        end = time.time()
        print(f"\nTool Chosen in {end - start:.2f} seconds")

        # Check tool_string for correct formatting and fix it if necessary
        if not tool_string.split()[0] == "{" or not tool_string.split()[-1] == "}":
            print("INCORRECT FORMAT DETECTED")
            print(f"Old format: {tool_string}")
            match = re.search(r"\{.*\}", tool_string, re.DOTALL)
            if match:
                tool_string = match.group()
                print(f"New format: {tool_string}")
        try:
            tool_object = json.loads(tool_string)
            # print("tool_object success")
            tool_function = TOOLS[tool_object["tool"]]
            # print("tool_function success")
            input_data = tool_object["inputdatavalue"]
            # print("input_data success")
            result = tool_function(input_data)
            # print("result success")
        except:
            print("\n-----------")   
            print("ERROR - tool_string could not be converted to tool_object")
            print(f"tool_string: {tool_string}")
            print("-----------\n")   
            return
        start = time.time()
        answer = self.generate_response(question, result)
        end = time.time()
        print(f"--- ANSWER ({end - start:.2f})---\n{answer}")

        

        

agent = Tool_Agent()

for _ in range(5):
    agent.answer_question("What is the temperature in New York?")
    agent.answer_question("Is it cold in Amsterdam?")
    agent.answer_question("Would you consider 36 to be young or old?")
    agent.answer_question("What do you think about an age of 16?")