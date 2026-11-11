# Instead of a scratchpad array in the agent class we can create a Memory class to replace it
# After all, memory.add() is much more readable than scratchpad.append()
from typing import List

class Memory:
    def __init__(self):
        self.observations: List[str] = []

    def add(self, observation: str):
        self.observations.append(
            observation
        )

    def get_all(self) -> List[str]:
        return self.observations