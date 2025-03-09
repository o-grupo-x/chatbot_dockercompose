import ollama

def chat_with_deepseek(prompt: str, history: list):
    """Handles conversation with DeepSeek via Ollama, including chat history."""
    try:
        response = ollama.chat(
            model="deepseek-r1",  
            messages=[
                {"role": "system", "content": "Você é um assistente que deve responser o mais rapido e direto possivel."},
                *history,
                {"role": "user", "content": prompt}
            ]
        )
        return response['message']
    except ollama._types.ResponseError as e:
        return f"DeepSeek model error: {e}"
