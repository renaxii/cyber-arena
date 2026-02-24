from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from simulation import GameState
from agents import call_model
import random

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")


# live single match
@app.get("/play")
def play_game():
    game = GameState()

    while not game.is_game_over():

        attacker_prompt = f"Stealth:{game.attacker_stealth} Security:{game.server_security} Choose: scan, exploit, hide."
        defender_prompt = f"Stealth:{game.attacker_stealth} Security:{game.server_security} Choose: patch, monitor."

        attacker_action = call_model("google/gemini-2.5-flash", attacker_prompt)["action"]
        defender_action = call_model("deepseek/deepseek-chat", defender_prompt)["action"]

        game.apply_turn(attacker_action, defender_action)

    if game.server_security <= 0:
        winner = "attacker (Gemini)"
    elif game.attacker_stealth <= 0:
        winner = "defender (DeepSeek)"
    else:
        winner = "timeout"

    return {
        "winner": winner,
        "history": game.history
    }


# research mode
@app.get("/simulate")
def simulate_games(n: int = 10):
    attacker_wins = 0
    defender_wins = 0
    timeouts = 0

    for _ in range(n):
        game = GameState()

        while not game.is_game_over():

            attacker_prompt = f"Stealth:{game.attacker_stealth} Security:{game.server_security} Choose: scan, exploit, hide."
            defender_prompt = f"Stealth:{game.attacker_stealth} Security:{game.server_security} Choose: patch, monitor."

            attacker_action = call_model("google/gemini-2.5-flash", attacker_prompt)["action"]
            defender_action = call_model("deepseek/deepseek-chat", defender_prompt)["action"]

            game.apply_turn(attacker_action, defender_action)

        if game.server_security <= 0:
            attacker_wins += 1
        elif game.attacker_stealth <= 0:
            defender_wins += 1
        else:
            timeouts += 1

    return {
        "games": n,
        "attacker_wins": attacker_wins,
        "defender_wins": defender_wins,
        "timeouts": timeouts,
        "attacker_winrate": attacker_wins / n
    }