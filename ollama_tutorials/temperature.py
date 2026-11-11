# You can adjust the temperature option by assigning a value between 0 and 1.
# The higher the temperature, the more creative the model's output will be.
# Note that regardless of temperature, the model will adhere to formatting criteria passed through the format parameter.
from ollama import chat
from pydantic import BaseModel

class Country(BaseModel):
  name: str
  capital: str
  languages: list[str]

# response0 = chat(
#   model='qwen3.5:4b',
#   messages=[{'role': 'user', 'content': 'Tell me about Canada.'}],
#   format=Country.model_json_schema(),
#   options={'temperature': 0},
# )
response50 = chat(
  model='qwen3.5:4b',
  messages=[{'role': 'user', 'content': 'Tell me about Canada.'}],
  format=Country.model_json_schema(),
  options={'temperature': 0.5},
)
# response100 = chat(
#   model='qwen3.5:4b',
#   messages=[{'role': 'user', 'content': 'Tell me about Canada.'}],
#   format=Country.model_json_schema(),
#   options={'temperature': 1},
# )

# country0 = Country.model_validate_json(response0.message.content)
country50 = Country.model_validate_json(response50.message.content)
# country100 = Country.model_validate_json(response100.message.content)

# print(f"country0: {country0}")
print(f"country50: {country50.model_dump()}, type: {type(country50.model_dump())}")
print(f"response50: {response50.message.content}, type: {type(response50.message.content)}")

# print(f"country100: {country100}")