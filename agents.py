from openrouter import OpenRouter
import os
from dotenv import load_dotenv
import json
import random

load_dotenv()

API_KEY = os.getenv("HACKCLUB_API_KEY")

client = OpenRouter(
    api_key=API_KEY,
    server_url="https://ai.hackclub.com/proxy/v1",
)


def call_model(model_name: str, prompt: str) -> dict:
    """Call an AI model with a prompt, return JSON"""
    try:
        response = client.chat.send(
            model=model_name,
            messages=[
                {"role": "system", "content": "Return ONLY valid JSON with no extra text."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except:
        return {"action": "hide", "target": "none"}  # Safe fallback


class AIAttacker:
    """Base class for attacker AI"""
    def __init__(self, name: str, model: str, strategy: str = "balanced"):
        self.name = name
        self.model = model
        self.strategy = strategy
        
    def choose_action(self, game_state) -> dict:
        """Choose an action based on game state"""
        raise NotImplementedError


class SmartAttacker(AIAttacker):
    """Uses AI model to decide actions strategically"""
    def __init__(self, name: str = "SmartAttacker", model: str = "google/gemini-2.5-flash"):
        super().__init__(name, model, "smart")
        
    def choose_action(self, game_state) -> dict:
        state_str = game_state.get_state_string()
        prompt = f"""You are a sophisticated cyberattacker. Your goal is to breach all systems.

Current state: {state_str}

Systems available: web_server, database, firewall

Available actions:
- "scan" (low risk, costs 5 resources, reveals system info)
- "exploit" (medium risk, costs 20 resources, damage 20-40)
- "brute_force" (high risk, costs 30 resources, damage 50, high stealth loss)
- "hide" (restore stealth, costs 5 resources, adds 15 stealth)

Choose the best strategy. Respond with JSON:
{{"action": "scan|exploit|brute_force|hide", "target": "web_server|database|firewall"}}"""
        
        return call_model(self.model, prompt)


class AggressiveAttacker(AIAttacker):
    """Aggressive strategy - prioritizes damage over stealth"""
    def __init__(self, name: str = "AggressiveAttacker"):
        super().__init__(name, "google/gemini-2.5-flash", "aggressive")
        
    def choose_action(self, game_state) -> dict:
        # Prioritize attacking vulnerable systems
        breached = [name for name, s in game_state.systems.items() if s.is_breached]
        vulnerable = [name for name, s in game_state.systems.items() if not s.is_breached and s.security < 60]
        
        if game_state.attacker_stealth < 20:
            return {"action": "hide", "target": "none"}
        elif vulnerable:
            # Attack the most vulnerable
            target = min(vulnerable, key=lambda n: game_state.systems[n].security)
            return {"action": "exploit", "target": target}
        elif game_state.attacker_resources > 50:
            return {"action": "brute_force", "target": "database"}
        else:
            return {"action": "scan", "target": "firewall"}


class StealthyAttacker(AIAttacker):
    """Stealthy strategy - prioritizes staying undetected"""
    def __init__(self, name: str = "StealthyAttacker"):
        super().__init__(name, "deepseek/deepseek-chat", "stealthy")
        
    def choose_action(self, game_state) -> dict:
        if game_state.attacker_stealth < 60:
            return {"action": "hide", "target": "none"}
        elif game_state.turn % 3 == 0:  # Every 3rd turn, try an exploit
            return {"action": "exploit", "target": "web_server"}
        else:
            return {"action": "scan", "target": random.choice(list(game_state.systems.keys()))}


class RandomAttacker(AIAttacker):
    """Random strategy - unpredictable behavior"""
    def __init__(self, name: str = "RandomAttacker"):
        super().__init__(name, "none", "random")
        
    def choose_action(self, game_state) -> dict:
        actions = ["scan", "exploit", "hide", "brute_force"]
        targets = list(game_state.systems.keys())
        return {
            "action": random.choice(actions),
            "target": random.choice(targets)
        }


class AIDefender:
    """Base class for defender AI"""
    def __init__(self, name: str, model: str, strategy: str = "balanced"):
        self.name = name
        self.model = model
        self.strategy = strategy
        
    def choose_action(self, game_state) -> dict:
        """Choose a defense action"""
        raise NotImplementedError


class SmartDefender(AIDefender):
    """Uses AI model for strategic defense"""
    def __init__(self, name: str = "SmartDefender", model: str = "google/gemini-2.5-flash"):
        super().__init__(name, model, "smart")
        
    def choose_action(self, game_state) -> dict:
        state_str = game_state.get_state_string()
        prompt = f"""You are a cybersecurity defender protecting multiple systems.

Current state: {state_str}

Available actions:
- "patch" (strengthen a system, costs 15 resources, adds 25 security)
- "monitor" (detect attacker, costs 5 resources, reduces attacker stealth by 10-20)
- "restore" (full system restore if breached, costs 25 resources, major stealth hit)

Respond with JSON:
{{"action": "patch|monitor|restore", "target": "web_server|database|firewall"}}"""
        
        return call_model(self.model, prompt)


class ReactivDefender(AIDefender):
    """Reactive strategy - focuses on damaged systems"""
    def __init__(self, name: str = "ReactiveDefender"):
        super().__init__(name, "none", "reactive")
        
    def choose_action(self, game_state) -> dict:
        # Find the most damaged system
        damaged = [(name, s.security) for name, s in game_state.systems.items() 
                  if not s.is_breached]
        
        if not damaged:
            return {"action": "monitor", "target": "firewall"}
        
        target = min(damaged, key=lambda x: x[1])[0]
        
        if game_state.systems[target].security < 30:
            return {"action": "patch", "target": target}
        else:
            return {"action": "monitor", "target": target}


class AggressiveDefender(AIDefender):
    """Aggressive strategy - prioritizes attack detection"""
    def __init__(self, name: str = "AggressiveDefender"):
        super().__init__(name, "none", "aggressive")
        
    def choose_action(self, game_state) -> dict:
        if game_state.turn < 5:
            return {"action": "monitor", "target": "firewall"}
        
        damaged = [name for name, s in game_state.systems.items() if s.security < 70]
        if damaged:
            return {"action": "patch", "target": damaged[0]}
        else:
            return {"action": "monitor", "target": "firewall"}


# Available agents for tournament
ATTACKERS = [
    SmartAttacker("Gemini-Smart", "google/gemini-2.5-flash"),
    AggressiveAttacker("Aggressive-Bot"),
    StealthyAttacker("Stealth-Ninja"),
    RandomAttacker("Chaos-Agent"),
]

DEFENDERS = [
    SmartDefender("Defender-Smart", "google/gemini-2.5-flash"),
    ReactivDefender("Reactive-Guard"),
    AggressiveDefender("Hunter-Bot"),
]