from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from simulation import GameState
from agents import ATTACKERS, DEFENDERS
import json
import asyncio

app = FastAPI()

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Tournament state
tournament_state = {
    "results": [],
    "leaderboard": {},
    "current_match": None
}


@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")


@app.get("/api/play")
def play_single_match(attacker_idx: int = 0, defender_idx: int = 0):
    """Play a single match between two AIs"""
    if attacker_idx >= len(ATTACKERS) or defender_idx >= len(DEFENDERS):
        return {"error": "Invalid agent index"}
    
    attacker = ATTACKERS[attacker_idx]
    defender = DEFENDERS[defender_idx]
    
    game = GameState(attacker.name, defender.name)
    
    while not game.is_game_over():
        attacker_action = attacker.choose_action(game)
        defender_action = defender.choose_action(game)
        game.apply_turn(attacker_action, defender_action)
    
    winner = game.get_winner()
    
    # Update scores
    if winner == "attacker":
        tournament_state["leaderboard"][attacker.name] = tournament_state["leaderboard"].get(attacker.name, 0) + 3
        tournament_state["leaderboard"][defender.name] = tournament_state["leaderboard"].get(defender.name, 0) + 0
    elif winner == "defender":
        tournament_state["leaderboard"][attacker.name] = tournament_state["leaderboard"].get(attacker.name, 0) + 0
        tournament_state["leaderboard"][defender.name] = tournament_state["leaderboard"].get(defender.name, 0) + 3
    else:
        tournament_state["leaderboard"][attacker.name] = tournament_state["leaderboard"].get(attacker.name, 0) + 1
        tournament_state["leaderboard"][defender.name] = tournament_state["leaderboard"].get(defender.name, 0) + 1
    
    result = {
        "winner": winner,
        "attacker": attacker.name,
        "defender": defender.name,
        "turns": game.turn - 1,
        "attacker_score": game.attacker_score,
        "final_stealth": game.attacker_stealth,
        "systems_breached": sum(1 for s in game.systems.values() if s.is_breached),
        "history": game.history
    }
    
    tournament_state["results"].append(result)
    return result


@app.get("/api/tournament")
def run_tournament():
    """Run a full round-robin tournament"""
    tournament_state["results"] = []
    tournament_state["leaderboard"] = {a.name: 0 for a in ATTACKERS}
    tournament_state["leaderboard"].update({d.name: 0 for d in DEFENDERS})
    
    results = []
    
    # Run each attacker vs each defender
    for attacker in ATTACKERS:
        for defender in DEFENDERS:
            game = GameState(attacker.name, defender.name)
            
            while not game.is_game_over():
                attacker_action = attacker.choose_action(game)
                defender_action = defender.choose_action(game)
                game.apply_turn(attacker_action, defender_action)
            
            winner = game.get_winner()
            
            # Award points
            if winner == "attacker":
                tournament_state["leaderboard"][attacker.name] += 3
            elif winner == "defender":
                tournament_state["leaderboard"][defender.name] += 3
            else:
                tournament_state["leaderboard"][attacker.name] += 1
                tournament_state["leaderboard"][defender.name] += 1
            
            result = {
                "attacker": attacker.name,
                "defender": defender.name,
                "winner": winner,
                "turns": game.turn - 1,
                "systems_breached": sum(1 for s in game.systems.values() if s.is_breached)
            }
            results.append(result)
            tournament_state["results"].append(result)
    
    # Sort leaderboard
    leaderboard = sorted(
        tournament_state["leaderboard"].items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    return {
        "matches": results,
        "leaderboard": leaderboard,
        "total_matches": len(results)
    }


@app.get("/api/agents")
def get_agents():
    """Get available agents"""
    return {
        "attackers": [{"name": a.name, "strategy": a.strategy} for a in ATTACKERS],
        "defenders": [{"name": d.name, "strategy": d.strategy} for d in DEFENDERS]
    }


@app.get("/api/leaderboard")
def get_leaderboard():
    """Get current leaderboard"""
    leaderboard = sorted(
        tournament_state["leaderboard"].items(),
        key=lambda x: x[1],
        reverse=True
    )
    return {"leaderboard": leaderboard}


@app.get("/api/results")
def get_results(limit: int = 50):
    """Get recent match results"""
    return {"results": tournament_state["results"][-limit:]}