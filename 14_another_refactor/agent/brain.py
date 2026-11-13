from ollama import chat
from pydantic import BaseModel, ValidationError

from typing import Any, Type, TypeVar

T = TypeVar("T", bound=BaseModel)

class StructuredOutputError(Exception):
    """Raised when the model fails to produce valid structured output after all retries."""

# Note how this class/method combination improves readability of the agent quite significantly by taking out the chonky chat() function
# Additionally, this class/method combination reduces repeated code, making it easier to make adjustments later on to, for example, the model.
class Brain:
    MODEL = "qwen3.5:4b"
    NUM_CTX = 16384         # Context window in tokens. Raise or lower this depending on `ollama ps`

    # Use think when the response is a simple data type that does not require validation.
    #   For example, when the model responds with a single word.
    def think(
            self,
            user_prompt: str,
            system_prompt: str | None = None,
            temperature: float = 0.5,            # Value between 0 and 1: higher = more creative output
            response_schema: dict[str, Any] | None = None,           # Either None or the output from a pydantic model's schema generator method
            think: bool = False                 # Set to True for debug logs
    ) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})

        response = chat(
            model=self.MODEL,
            messages=messages,
            tools=[],
            think=think,
            format=response_schema,
            options={'temperature': temperature, "num_ctx": self.NUM_CTX},
        )
        if think:
            print(f"----- THOUGHT PROCESS -----\n{response.message.thinking}")

        # Diagnostics: these two situations are the classic causes of broken JSON
        if response.done_reason == "length":
            print("[Brain] WARNING: the output was cut off because it hit the length limit.")
        if response.prompt_eval_count and response.prompt_eval_count >= 0.95 * self.NUM_CTX:
            print(f"[Brain] WARNING: the prompt used {response.prompt_eval_count} tokens, "
                  f"close to num_ctx={self.NUM_CTX}. It may have been truncated.")

        return (response.message.content or "").strip()

    # Use think_structured when you need to validate the output against a schema.
    #   For example when the model responds with a json object and the object should have specific keys and value types.
    def think_structured(
        self,
        response_model: Type[T],
        user_prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.5,
        max_retries: int = 3,
        think: bool = False,
    ) -> T:
        schema = response_model.model_json_schema()
        prompt = user_prompt
        last_error: ValidationError | None = None

        for attempt in range(1, max_retries + 1):
            raw = ""
            try:
                raw = self.think(
                    user_prompt=prompt,
                    system_prompt=system_prompt,
                    temperature=temperature,
                    response_schema=schema,
                    think=think
                )
                return response_model.model_validate_json(raw)
            except ValidationError as e:
                last_error = e
                print(
                    f"[Brain] Attempt {attempt}/{max_retries} failed validation for "
                    f"{response_model.__name__}.\n Raw output: {raw!r}\n Error: {e}"
                )
                prompt = (
                    f"{user_prompt}\n\n"
                    f"Your previous response was invalid:\n{str(e)[:500]}\n"
                    f"Return a corrected JSON object that matches the schema exactly."
                )

        raise StructuredOutputError(
            f"No valid {response_model.__name__} after {max_retries} attempts."
        ) from last_error