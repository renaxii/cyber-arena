from openrouter import OpenRouter
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("HACKCLUB_API_KEY")

client = OpenRouter(
    api_key=API_KEY,
    server_url="https://ai.hackclub.com/proxy/v1",
)

def call_gemini(prompt):
    response = client.chat.send(
        model="google/gemini-2.5-flash",
        messages=[
            {
                "role": "system",
                "content": "You are an AI agent in a cybersecurity simulation. You must respond ONLY with valid JSON. No explanations. No extra text."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={"type": "json_object"}
    )

    return response.choices[0].message.content