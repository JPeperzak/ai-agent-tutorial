import json
from ollama import chat
from jsonschema import validate

from agent.prompts import (
    SYSTEM_PROMPT_ARGUMENT_GENERATION,
    SYSTEM_PROMPT_FINAL_ANSWER,
    SYSTEM_PROMPT_TOOL_SELECTION,
    build_argument_user_prompt,
    build_final_answer_user_prompt,
    build_tool_selection_user_prompt
)

class Executor:
    def __init__(self, registry):
        self.registry = registry

    def select_tool(
            self,
            state
    ):
        user_prompt = build_tool_selection_user_prompt(state.user_request, self.registry)
        response = chat(
            model="qwen3.5:4b",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT_TOOL_SELECTION
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )
        data = json.loads(response.message.content.strip())
        state.selected_tool = data["tool"]

    def generate_arguments(
        self,
        state
    ):
        user_prompt = build_argument_user_prompt(state.user_request, state.selected_tool, self.registry)
        response = chat(
            model="qwen3.5:4b",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT_ARGUMENT_GENERATION
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )
        state.tool_args = json.loads(response.message.content.strip())

    def validate_tool_args(self, state):
        schema = self.registry[state.selected_tool]["schema"]

        validate(
            instance=state.tool_args,
            schema=schema
        )

    def execute_tool(
        self,
        state
    ):
        self.validate_tool_args(state)
        tool_info = self.registry[state.selected_tool]
        tool = tool_info["function"]
        result = tool(**state.tool_args)
        state.observations.append(
            f"{state.selected_tool}: {result}"
        )

        state.selected_tool = None
        state.tool_args = None

        if result:
            state.final_answer = str(result)