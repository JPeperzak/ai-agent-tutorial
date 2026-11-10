from agent import Agent

agent = Agent()

for _ in range(1):
    print(agent.answer_question("What is docker?"))
    print("\n" + 30*"-" + "\n")
    print(agent.answer_question("What is python?"))
    print("\n" + 30*"-" + "\n")
    print(agent.answer_question("What is ai?"))
    print("\n" + 30*"-" + "\n")