import json

from typing import Any, Dict

def generate_select_action_user_prompt(
        goal: str, 
        observations_text: str,
        executed_actions_text: str,
        tool_registry: Dict[str, Dict[str, Any]],
    ) -> str:
    tools = []

    for name, tool in tool_registry.items():
        tools.append(
            f"- {name}: {tool['description']}"
        )

    return f"""
User request:
{goal}

Available tools:
{"\n".join(tools)}

Actions taken:
{executed_actions_text}

Observations:
{observations_text}
"""

def generate_tool_selection_user_prompt(
        goal: str, 
        observations_text: str, 
        executed_actions_text: str,
        tool_registry: Dict[str, Dict[str, Any]]
    ) -> str:
    tools = []

    for name, tool in tool_registry.items():
        tools.append(
            f"- {name}: {tool['description']}"
        )

    return f"""
User request:
{goal}

Actions taken:
{executed_actions_text}

Observations:
{observations_text}
    
Available tools:
{"\n".join(tools)}
"""

def generate_arguments_user_prompt(
        goal: str, 
        observations_text: str, 
        executed_actions_text: str,
        selected_tool: str, 
        tool_registry: Dict[str, Dict[str, Any]]
    ) -> str:
    schema = tool_registry[selected_tool]["schema"]

    return f"""
User request:
{goal}

Actions taken:
{executed_actions_text}
    
Selected tool:
{selected_tool}

Argument schema:
{json.dumps(schema, indent=2)}

Observations:
{observations_text}
"""

def generate_final_answer_user_prompt(
        goal: str, 
        observations_text: str
    ) -> str:
    return f"""
User request:
{goal}

Observations:
{observations_text}
"""