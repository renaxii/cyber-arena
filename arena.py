from simulation import GameState
from agents import call_gemini
import json

def get_attacker_action(state):
    prompt = f"""
You are a hacker agent.

Current state:
- Your stealth level: {state.attacker_stealth}
- Target server security: {state.server_security}

Choose ONE action:
- "scan"
- "exploit"
- "hide"

Respond in JSON like this:
{{
  "action": "scan"
}}
"""

    response = call_gemini(prompt)
    parsed = json.loads(response)
    return parsed["action"]


if __name__ == "__main__":
    game = GameState()

    while not game.is_game_over():
        game.print_state()

        action = get_attacker_action(game)
        print(f"\nGemini chooses: {action}")

        game.apply_action(action)

    print("\n=== GAME OVER ===")

    if game.server_security <= 0:
        print("Attacker wins!")
    elif game.attacker_stealth <= 0:
        print("Defender wins!")
    else:
        print("Time limit reached!")