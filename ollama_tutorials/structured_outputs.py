# You can specify specific output structures using the "format" parameter in the chat function.
from ollama import chat
from pydantic import BaseModel

response = chat(
  model='qwen3.5:4b',
  messages=[{'role': 'user', 'content': 'Tell me about Canada.'}],
  format='json'
)
print(response.message.content)

# Notice how the first response, while always in json, still varies in content.
# Whereas this second response always follows the same three-attribute structure.
class Country(BaseModel):
  name: str
  capital: str
  languages: list[str]

response = chat(
  model='qwen3.5:4b',
  messages=[{'role': 'user', 'content': 'Tell me about Canada.'}],
  format=Country.model_json_schema(),
)

country = Country.model_validate_json(response.message.content)
print(country)

# You can also define the objects you want returned and let the model populate the fields:
class Pet(BaseModel):
  name: str
  animal: str
  age: int
  color: str | None
  favorite_toy: str | None

class PetList(BaseModel):
  pets: list[Pet]

response = chat(
  model='qwen3.5:4b',
  messages=[{'role': 'user', 'content': 'I have two cats named Luna and Loki...'}],
  format=PetList.model_json_schema(),
)

pets = PetList.model_validate_json(response.message.content)
print(pets)