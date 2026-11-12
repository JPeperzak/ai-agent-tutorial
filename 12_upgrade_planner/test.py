x = [{"description": "task1", "completed": False}, {"description": "task2", "completed": False}]

y = map(lambda step: step["description"], x)
z = [step["description"] for step in x]
a = "\n".join([step["description"] for step in x])


print(list(y))
print(z)
print(a)
