from ollama import chat
from pydantic import BaseModel

class GeneratedArguments(BaseModel):
    arguments: dict[str, str|int] | None
    otherattribute: str

schema_fields = GeneratedArguments.model_fields.keys()


print(GeneratedArguments.model_fields)
print(type(GeneratedArguments.model_fields))

# response = chat(
#   model='qwen3.5:4b',
#   messages=[{'role': 'user', 'content': 'Give me five examples of words that sound alike'}],
#   format=GeneratedArguments.model_json_schema(),
#   options={'temperature': 0.5},
# )


# response = GeneratedArguments.model_validate_json(response.message.content)

# print(f"country50: {response}, type: {type(response)}")
