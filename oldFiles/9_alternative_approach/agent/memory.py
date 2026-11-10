class Memory:
    def __init__(self):
        self.observations = []

    def add(self, observation):
        self.observations.append(
            observation
        )

    def get_all(self):
        return self.observations