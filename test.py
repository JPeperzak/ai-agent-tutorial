from pydantic import BaseModel

class PlanStepModel(BaseModel):
    description: str
    completed: bool = False

class PlanModel(BaseModel):
    steps: list[PlanStepModel]

x = PlanModel(steps=[PlanStepModel(description="yay", completed=False)])
if x.steps:
    print("yay")
else:
    print("nay")