# Instead of a scratchpad array in the agent class we can create a Memory class to replace it
# After all, memory.add() is much more readable than scratchpad.append()

class Memory:
    def __init__(self):
        self.observations = []

    def add(self, observation):
        self.observations.append(
            observation
        )

    def get_all(self):
        return self.observations