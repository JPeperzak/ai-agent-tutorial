from ollama import chat

class Agent:
    def __init__(self):
        self.energy = 100
        self.money = 0

        # We can create storage for past interactions that serves as "memory" for the agent
        self.memory = []

    def remember(self, event):
        self.memory.append(event)

    def show_memory(self):
        print("\nMemory:")

        for memory in self.memory:
            print(f"- {memory}")

    # It is good practice to separate the observation gathering from the prompt construction to keep the code organized as the project grows
    def observe(self):
        return {
            "energy": self.energy,
            "money": self.money
        }

    def build_prompt(self):
        state = self.observe()
        recent_memories = "\n".join(self.memory[-5:])
        return f"""
Current state:

Energy: {state["energy"]}
Money: {state["money"]}

Recent memories:

{recent_memories}

What should I do?
"""

    # The think method is where we contact the model to get a response
    # Note how the prompt is built in the think method because it's needed for the user message
    def think(self):
        prompt = self.build_prompt()
        response = chat(
            model="qwen2.5:0.5b",
            messages=[
                {
                    "role": "system",
                    "content": (
                "You are an office worker. "
                "You may only repond with "
                "'work', 'rest', or 'eat'."
            )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response["message"]["content"]

    def act(self, decision):
        if decision == "work":
            print("Working...")
            self.energy -= 23
            self.money += 10
            self.remember(
                "Worked and earned €10"
            )

        elif decision == "rest":
            print("Resting...")
            self.energy += 25
            self.remember(
                "Rested to regain energy"
            )

        elif decision == "eat":
            print("Eating...")
            self.energy += 50
            self.money -= 20
            self.remember(
                "Spent money to eat and regain energy"
            )

    def run(self):
        self.observe()
        decision = self.think()
        print(f"Decision: {decision}")
        self.act(decision)

agent = Agent()

for _ in range(10):
    agent.run()
    print("-" * 30)

agent.show_memory()