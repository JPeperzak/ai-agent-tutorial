from agent import Agent

agent = Agent()

for _ in range(3):
    print(agent.answer_question("What files exist?"))
    print("\n" + 30*"-" + "\n")
    print(agent.answer_question("What is the content of readme.py?"))
    print("\n" + 30*"-" + "\n")
    print(agent.answer_question("How many lines are in agent.py?"))
    print("\n" + 30*"-" + "\n")