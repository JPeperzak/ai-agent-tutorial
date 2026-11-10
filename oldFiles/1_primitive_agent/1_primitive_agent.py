# This class represents a Rule-Based AI agent: intelligence comes from rules a programmer writes
# Despite this agent being very primitive, llm's do the same thing conceptually: Observe -> Think -> Act
class primitiveAgent:
    # The agent has memory, remembering its energy between actions
    def __init__(self):
        self.energy = 100
        self.money = 0

    # The agent can gather information about the world and itself
    def observe(self):
        print(f"Energy: {self.energy}")
        print(f"Money: {self.money}")

    # The agent can act depending on its situation, based on what we call a "decision policy"
    def think(self):
        if self.energy < 30:
            if self.money >= 20:
                return "eat"
            return "rest"
        return "work"

    # The way the agent acts changes the world through consequences.
    def act(self, decision):
        if decision == "work":
            print("Working...")
            self.energy -= 15
            self.money += 10

        elif decision == "rest":
            print("Resting...")
            self.energy += 25

        elif decision == "eat":
            print("Eating...")
            self.energy += 50
            self.money -= 20

    def run(self):
        self.observe()
        decision = self.think()
        print(f"Decision: {decision}")
        self.act(decision)

agent = primitiveAgent()

for _ in range(10):
    agent.run()
    print("-" * 30)