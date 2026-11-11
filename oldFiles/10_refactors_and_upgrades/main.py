from agent.agent import Agent

agent = Agent()

for _ in range (1):
    print("\n" + 30*"-" + "\n")
    print(agent.answer_question("Tell me about containers."))
    print("\n" + 30*"-" + "\n")
    print(agent.answer_question("What are the traditional goals of AI research?"))
    print("\n" + 30*"-" + "\n")
    print(agent.answer_question("Tell me about how docker can be used in Python."))
    print("\n" + 30*"-" + "\n")
    print(agent.answer_question("Tell me how many files related to the agent's source code start with the letter 'p'."))
    print("\n" + 30*"-" + "\n")
