from ollama import chat

# Note how this class/method combination improves readability of the agent quite significantly by taking out the chonky chat() function
# Additionally, this class/method combination reduces repeated code, making it easier to make adjustments later on to, for example, the model.
class Brain:
    def think(
            self,
            system_prompt,
            user_prompt
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
            ]
        )
        return response.message.content.strip()