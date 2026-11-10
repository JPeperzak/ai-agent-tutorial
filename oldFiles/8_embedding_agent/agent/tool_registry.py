from tools.file_tools import (
    list_files,
    count_lines,
    read_file
)

from tools.rag_tools import (
    search_documents,
    read_document,
    SemanticSearchTool
)

def build_tool_registry(
    embedder,
    vector_store
):
    semantic_search_tool = SemanticSearchTool(embedder, vector_store)
    return {
    "list_files": {
        "function": list_files,
        "description": "Returns all project files related to the agent's source code",
        "arguments": {}
    },
    "count_lines": {
        "function": count_lines,
        "description": "Returns the number of lines in a file related to the agent's source code.",
        "arguments": {
            "filename": "Name of the file."
        }
    },
    "read_file": {
        "function": read_file,
        "description": "Returns the full contents of a file related to the agent's source code.",
        "arguments": {
            "filename": "Name of the file."
        }
    },
    "search_documents": {
        "function": search_documents,
        "description": (
            "Performs keyword-based document search. "
            "Use when you need exact word matches."
        ),
        "arguments": {
            "query": (
                "A search term or topic to look for, "
                "such as 'refund policy', 'docker', or 'python'."
            )
        }
    },
    "read_document": {
        "function": read_document,
        "description": (
            "Reads the contents of a specific document and returns "
            "its full text. Use this after identifying a document "
            "with search_documents."
        ),
        "arguments": {
            "filename": (
                "The name of the document to read, "
                "for example 'refund_policy.txt'."
            )
        }
    },
    "semantic_search": {
        "function": semantic_search_tool,
        "description": (
            "Performs semantic similarity search across the knowledge base. "
            "Returns the most relevant content even when the query uses "
            "different wording than the document. Prefer this tool for "
            "retrieving information from documents."
        ),
        "arguments": {
            "query": (
                "Natural language query."
            )
        }
    }
    }



# This function creates the list of available tools used in the user_prompt
def build_tool_prompt(tools):
    # Every section in the sections array represents one tool
    sections = []

    # Note that here "name" refers to the key, and "metadata" to the value associated with it (aka the object)
    for name, metadata in tools.items():
        section = [
            f"Tool: {name}",
            f"Description: {metadata["description"]}"
        ]
        arguments = metadata["arguments"]

        if arguments:
            section.append("Arguments:")
            for arg, description in arguments.items():
                section.append(
                    f"- {arg}: {description}"
                )

        sections.append("\n".join(section))

    return "\n\n".join(sections)