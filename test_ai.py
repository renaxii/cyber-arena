from agents import call_gemini
import json

if __name__ == "__main__":
    prompt = """
You are a hacker agent.

Current state:
- Your stealth level: 80
- Target server security: 60

Choose ONE action:
- "scan"
- "exploit"
- "hide"

Respond in JSON like this:
{
  "action": "scan"
}
"""

    result = call_gemini(prompt)

    print("Raw model output:")
    print(result)

    print("\nParsed JSON:")
    parsed = json.loads(result)
    print(parsed)