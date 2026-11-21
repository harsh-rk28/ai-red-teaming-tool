import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# quick check with a short message that API key and model work before running real attacks
response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {"role": "user", "content": "Say hello and tell me one fun fact about the ocean."} 
    ]
)

print(response.choices[0].message.content)

