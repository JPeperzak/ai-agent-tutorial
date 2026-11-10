AGENT_SYSTEM_PROMPT = """
You are an autonomous agent.

Your job is to solve the user's goal by:

1. Examining previous observations.
2. Choosing tools when needed.
3. Continuing until enough information has been gathered.
4. Producing a final answer.

Available response formats:

Tool call:

{
    "tool": "search_documents",
    "query": "docker"
}

or

{
    "tool": "read_document",
    "filename": "ai.txt"
}

Final answer:

{
    "action": "answer",
    "response": "your answer"
}

Rules:

- Respond with JSON only.
- Never explain your reasoning.
- Never include markdown.
- Never include code fences.
"""

def generate_decide_next_step_user_prompt(question, observations):
    return f"""
Goal:

{question}

Previous Observations:

{observations}

Available Tools:

search_documents
    Returns all project files whose name contains the query value.

read_document
    Returns the content of a specified file.

Decide what to do next.
"""