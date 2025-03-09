from openai import OpenAI
from config import Config

client = OpenAI(api_key=Config.OPENAI_API_KEY)

def chat_with_gpt(prompt: str, history: list, model="gpt-4o-mini", max_tokens=50):
    """Handles conversation with OpenAI GPT, including chat history."""
    messages = [{"role": "system", "content": "Você é um assistente útil."}]

    for msg in history:
        messages.append({"role": "user", "content": msg["user"]})
        messages.append({"role": "assistant", "content": msg["bot"]})

    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens
    )

    return response.choices[0].message.content.strip()
