from pydantic import BaseModel
from typing import Literal

class PlanStepModel(BaseModel):
    description: str
    completed: bool = False

class PlanModel(BaseModel):
    steps: list[PlanStepModel]

class ActionSelectionModel(BaseModel):
    action: Literal["tool", "complete_step", "done"]
    reasoning: str

class CriticDecisionModel(BaseModel):
    response: Literal["enough", "more", "exhausted"]
    reasoning: str
    missing_information: str

class FinalAnswerModel(BaseModel):
    response: str

# Models used for extract_facts() 
class FactModel(BaseModel):
    statement: str

class FactExtractionModel(BaseModel):
    facts: list[FactModel]