# The prompts.py file is useful to keep the prompts out of the business logic, increasing the readability of the code.

# Notice how we've expanded this prompt by adding examples and specifying output format
TOOL_SELECTION_PROMPT = """
You are a tool selector.

Available tools:

list_files
read_file
count_lines

Respond using ONLY JSON.

Examples:

{
    "tool": "list_files"
}

{
    "tool": "read_file",
    "filename": "agent.py"
}
"""

ANSWER_PROMPT = """
Answer the user using the provided tool result.
"""

def generate_user_answer_prompt(question, result):
    return f"""
Question:
{question}

Tool Result:
{result}
"""