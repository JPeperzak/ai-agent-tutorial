import json

from typing import Any
from agent.models.data_types import (
    MemoryFact
)

from agent.prompts.helpers import format_facts

def generate_arguments_user_prompt(
        goal: str,
        current_step_description: str,
        plan_text: str,
        observations_text: str, 
        facts: list[MemoryFact],
        executed_actions_text: str,
        selected_tool: str, 
        tool_registry: dict[str, dict[str, Any]]
    ) -> str:
    schema = tool_registry[selected_tool]["schema"]

    return f"""USER REQUEST:
{goal}

PLAN:
{plan_text}

CURRENT STEP:
{current_step_description}

PREVIOUS ACTIONS TAKEN:
{executed_actions_text}
    
SELECTED TOOLS:
{selected_tool}

ARGUMENT SCHEMA:
{json.dumps(schema, indent=2)}

KNOWN FACTS:
{format_facts(facts)}

RECENT OBSERVATIONS:
{observations_text}
"""

def generate_user_prompt(
        goal: str,
        observations_text: str | None = None,
        facts: list[MemoryFact] | None = None,
        current_step_description: str | None = None,
        plan_text: str | None = None,
        executed_actions_text: str | None = None,
        tool_registry: dict[str, dict[str, Any]] | None = None,
) -> str:
    if tool_registry:
        tools = []
        
        for name, tool in tool_registry.items():
            tools.append(
                f"- {name}\n\t{tool['description']}"
            )

    prompt = f"USER REQUEST:\n{goal}"
    prompt += f"\n\nPLAN:\n{plan_text}" if plan_text else ""
    prompt += f"\n\nCURRENT STEP:\n{current_step_description}" if current_step_description else ""
    prompt += f"\n\nPREVIOUS ACTIONS TAKEN:\n{executed_actions_text}" if executed_actions_text else ""
    prompt += f"\n\nAVAILABLE TOOLS:\n{"\n".join(tools)}" if tool_registry else ""
    prompt += f"\n\nKNOWN FACTS:\n{format_facts(facts)}" if facts else ""
    prompt += f"\n\nRECENT OBSERVATIONS:\n{observations_text}" if observations_text else ""
    return prompt

def generate_facts_user_prompt(
        retrieved_information: str
) -> str:
    return f"""Extract factual information from the text.

Rules:

- Keep facts concise.
- Do not invent information.
- Remove explanations.
- Remove repetitions.
- One idea per fact.

Text:

{retrieved_information}
"""
