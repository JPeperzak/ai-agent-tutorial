import time
from typing import List
from ollama import chat, Message

from oldFiles.tools import get_temperature

class Complicated_Tool_Agent:
    def __init__(self):
        self.memory: List[str] = []

    def remember(self, event: str):
        self.memory.append(event)

    def show_memory(self):
        print("\nMemory:")
        for memory in self.memory:
            print(f"- {memory}")

    def build_prompt(self, location: str):
        return f"What is the temperature in {location}?"

    def think(self):
        prompt = self.build_prompt("New York")
        messages: List[Message] = [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        response = chat(
            model="qwen3.5:4b",
            messages=messages,
            tools=[get_temperature],
            think=True
        )

        messages.append(response.message)
        if response.message.tool_calls:
            call = response.message.tool_calls[0]
            result = get_temperature(**call.function.arguments)
            messages.append({"role": "tool", "tool_name": call.function.name, "content": str(result)})
            final_response = chat(model="qwen3.5:4b", messages=messages, tools=[get_temperature], think=True)
            return final_response.message.content
        return response["message"]["content"]

    def act(self, decision):
        print("RESPONSE")
        print(decision)

    def run(self):
        start = time.time()
        decision = self.think()
        end = time.time()
        print(f"Response took {end - start:.2f} seconds")
        self.act(decision)

agent = Complicated_Tool_Agent()

for _ in range(2):
    agent.run()
    print("-" * 30)