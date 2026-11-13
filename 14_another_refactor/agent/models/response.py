from pydantic import BaseModel
from enum import StrEnum

class Action(StrEnum):
    TOOL = "tool"
    COMPLETE_STEP = "complete_step"
    DONE = "done"

class CriticVerdict(StrEnum):
    ENOUGH = "enough"
    MORE = "more"
    EXHAUSTED = "exhausted"


class PlanStepModel(BaseModel):
    description: str
    completed: bool = False

class PlanModel(BaseModel):
    steps: list[PlanStepModel]

class ActionSelectionModel(BaseModel):
    action: Action
    reasoning: str

class CriticDecisionModel(BaseModel):
    response: CriticVerdict
    reasoning: str
    missing_information: str

class FinalAnswerModel(BaseModel):
    response: str

# Models used for extract_facts() 
class FactModel(BaseModel):
    statement: str

class FactExtractionModel(BaseModel):
    facts: list[FactModel]