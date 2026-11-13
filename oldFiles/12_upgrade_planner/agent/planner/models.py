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