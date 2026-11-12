import json

from typing import Any, Dict

def generate_arguments_user_prompt(
        goal: str,
        current_step_description: str,
        plan_text: str,
        observations_text: str, 
        executed_actions_text: str,
        selected_tool: str, 
        tool_registry: Dict[str, Dict[str, Any]]
    ) -> str:
    schema = tool_registry[selected_tool]["schema"]

    return f"""USER REQUEST:
{goal}

PLAN:
{plan_text}

CURRENT STEP:
{current_step_description}

ACTIONS TAKEN:
{executed_actions_text}
    
SELECTED TOOLS:
{selected_tool}

ARGUMENT SCHEMA:
{json.dumps(schema, indent=2)}

OBSERVATIONS:
{observations_text}
"""

def generate_user_prompt(
        goal: str,
        observations_text: str, 
        current_step_description: str | None = None,
        plan_text: str | None = None,
        executed_actions_text: str | None = None,
        tool_registry: Dict[str, Dict[str, Any]] | None = None,
) -> str:
    if tool_registry:
        tools = []
        
        for name, tool in tool_registry.items():
            tools.append(
                f"- {name}: {tool['description']}"
            )
    prompt = f"USER REQUEST:\n{goal}"
    prompt += f"\n\nPLAN:\n{plan_text}" if plan_text else ""
    prompt += f"\n\nCURRENT STEP:\n{current_step_description}" if current_step_description else ""
    prompt += f"\n\nACTIONS TAKEN:\n{executed_actions_text}" if executed_actions_text else ""
    prompt += f"\n\nAVAILABLE TOOLS:\n{"\n".join(tools)}" if tool_registry else ""
    prompt += f"\n\nOBSERVATIONS:\n{observations_text}"
    return prompt