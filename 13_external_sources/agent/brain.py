from ollama import chat

from typing import Any, Dict

# Note how this class/method combination improves readability of the agent quite significantly by taking out the chonky chat() function
# Additionally, this class/method combination reduces repeated code, making it easier to make adjustments later on to, for example, the model.
class Brain:
    def think(
            self,
            user_prompt: str,
            system_prompt: str | None = None,
            temperature: float = 0.5,            # Value between 0 and 1: higher = more creative output
            response_schema: Dict[str, Any] | None = None,           # Either None or the output from a pydantic model's schema generator method
            think: bool = False                 # Set to True for debug logs
    ):

        response = chat(
            model="qwen3.5:4b",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            tools=[],
            think=think,
            format=response_schema,
            options={'temperature': temperature},
        )
        if think:
            print(f"----- THOUGHT PROCESS -----\n{response.message.thinking}")

        
        return response.message.content.strip()