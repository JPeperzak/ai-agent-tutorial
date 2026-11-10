# Ollama is a package that allows you to run local models such as the Qwen model
from ollama import chat

response = chat(
    model="qwen3:4b",
    # The content of "messages" is the conversation we're sending to the model. The model predicts an answer based on its contents.
    # Every object passed to the messages array represents one message in the conversation history.
    # e.g. if you asked AI how they're doing and they respond they're doing well, that totals up to 2 objects in the messages array. 

    # Additionally, you pass a "role" along with the content of the message. This role tells the model how to interpret the message:
    #   - "system" is interpreted as the model's instructions: it defines the rules, behavior, and personality of the model.
    #   - "user" represents the information coming from the outside world. This could be a conversational sentence for a chatbot or flat data for another agent.
    #           Turning program state into language is called "serialization".
    #   - "assistant" represents previous model responses. If the AI previously responded they're doing well, that message will have the role of assistant.
    messages=[
        {
            "role": "system",
            "content": (
                "You are an office worker. "
                "You may only repond with "
                "'work', 'rest', or 'eat'."
            ),
        },
        {
            "role": "user",
            "content": (
                "Energy=20 "
                "Money=100"
            ),
        },
    ]
)

print(response["message"]["content"])