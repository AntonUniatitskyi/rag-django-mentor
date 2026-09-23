import litellm
import config

def call_llm(system_prompt: str, messages: list[dict]) -> str:
    full_messages = [
        {"role": "system", "content": system_prompt},
        *messages,
    ]
    response = litellm.completion(
        model=config.PRIMARY_MODEL,
        fallbacks=config.FALLBACK_MODELS,
        messages=full_messages,
        temperature=0.3,
    )
    return response["choices"][0]["message"]["content"]