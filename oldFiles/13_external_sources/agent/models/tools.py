from pydantic import BaseModel, Field

class RetrieveKnowledgeModel(BaseModel):
    query: str = Field(description="The specific question or keywords to find within the local knowledge database.")

# Notice the use of Field in this basemodel. 
# The Field descriptions end up in the JSON schema, so the model sees them in both the prompt and the constrained output format.
class SearchWikipediaModel(BaseModel):
    topic: str = Field(description="Title of the Wikipedia article to look up. Keep it short, e.g. 'Docker (software)'.")
    query: str = Field(description="The specific question or keywords to find within that article.")

class SearchWebModel(BaseModel):
    query: str  = Field(description="A short web search query of 3 to 8 words, e.g. 'docker compose use cases'.")