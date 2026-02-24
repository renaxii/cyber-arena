from openrouter import OpenRouter
import os
from dotenv import load_dotenv
import json

load_dotenv()

API_KEY = os.getenv("HACKCLUB_API_KEY")

client = OpenRouter(
    api_key=API_KEY,
    server_url="https://ai.hackclub.com/proxy/v1",
)

def call_model(model_name, prompt):
    response = client.chat.send(
        model=model_name,
        messages=[
            {"role": "system", "content": "Return ONLY valid JSON."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)