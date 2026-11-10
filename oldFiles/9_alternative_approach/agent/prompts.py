import json

SYSTEM_PROMPT_TOOL_SELECTION = """
You are a tool selection assistant.

Your task is to choose the single best tool for the user's request.

Rules:
- Select exactly one tool.
- Do not generate arguments.
- Do not explain your choice.
- Return JSON only.
- Return exactly one JSON object.

Response format:

{
    "tool": "<tool_name>"
}
"""

SYSTEM_PROMPT_ARGUMENT_GENERATION = """
You are an argument extraction assistant.

Your task is to generate valid arguments for the selected tool.

Rules:
- Generate arguments only.
- Do not choose a tool.
- Do not explain your reasoning.
- Return JSON only.
- Return exactly one JSON object.
- Follow the provided schema.

If information is missing, return:

{
    "error": "missing_required_information"
}
"""

SYSTEM_PROMPT_FINAL_ANSWER = """
You are an answer generation assistant.

Your job is to answer the user's request using the supplied observations.

Rules:
- Use the provided observations.
- Do not invent information.
- Do not reference tools.
- Return JSON only.
- Return exactly one JSON object.

Response format:

{
    "action": "answer",
    "response": "<answer>"
}
"""

# This prompt builder creates a prompt exclusively for selecting a tool.
# The goal is to simplify the decision-making process for the agent by focusing solely on tool selection, rather than combining several tasks.
def build_tool_selection_user_prompt(user_request, registry):
    tools = []

    for name, tool in registry.items():
        tools.append(
            f"- {name}: {tool['description']}"
        )

    return f"""
Choose the best tool.

Available tools:

{chr(10).join(tools)}

User request:
{user_request}

Return JSON:

{{
    "tool": "<tool_name>"
}}
"""

def build_argument_user_prompt(user_request, tool_name, registry):
    schema = registry[tool_name]["schema"]

    return f"""
Generate arguments for the selected tool.

Tool:
{tool_name}

Argument schema:
{json.dumps(schema, indent=2)}

User request:
{user_request}

Return JSON matching the schema exactly.
"""

def build_final_answer_user_prompt(user_request, observations):
    observations_text = "\n".join(
        observations
    )
    return f"""
User request:
{user_request}

Observations:
{observations_text}
"""