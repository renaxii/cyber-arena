import random
from enum import Enum
from dataclasses import dataclass

MAX_TURNS = 15


class System:
    """Represents a target system with security and exploit progress"""
    def __init__(self, name: str, security: int = 100):
        self.name = name
        self.security = security
        self.max_security = security
        self.exploit_progress = 0
        self.is_breached = False
        
    def take_damage(self, amount: int):
        self.security = max(0, self.security - amount)
        if self.security <= 0:
            self.is_breached = True
            
    def repair(self, amount: int):
        self.security = min(self.max_security, self.security + amount)


class GameState:
    """Enhanced game state with multiple systems and agents"""
    def __init__(self, attacker_name: str = "Attacker", defender_name: str = "Defender"):
        self.attacker_name = attacker_name
        self.defender_name = defender_name
        self.attacker_stealth = 100
        self.attacker_resources = 100
        self.defender_resources = 100
        
        # Multiple systems to attack/defend
        self.systems = {
            "web_server": System("Web Server", 80),
            "database": System("Database", 120),
            "firewall": System("Firewall", 100),
        }
        
        self.turn = 1
        self.history = []
        self.attacker_score = 0
        self.defender_score = 0
        
    def get_state_string(self) -> str:
        """Returns a compact state description for AI prompts"""
        systems_str = " | ".join([
            f"{s.name}: {s.security}/{s.max_security}" if not s.is_breached 
            else f"{s.name}: BREACHED"
            for s in self.systems.values()
        ])
        return f"Stealth:{self.attacker_stealth} Resources:{self.attacker_resources} Defender:{self.defender_resources} Systems:[{systems_str}]"

    def apply_turn(self, attacker_action: dict, defender_action: dict):
        """Process one turn with both actions"""
        
        # Defender actions
        if defender_action.get("action") == "patch":
            target = defender_action.get("target", "web_server")
            if target in self.systems and not self.systems[target].is_breached:
                self.systems[target].repair(25)
                self.defender_resources -= 15
                
        elif defender_action.get("action") == "monitor":
            self.attacker_stealth -= random.randint(10, 20)
            self.defender_resources -= 5
            
        elif defender_action.get("action") == "restore":
            self.attacker_stealth -= 30
            self.defender_resources -= 25
        
        # Attacker actions
        action = attacker_action.get("action", "scan")
        
        if action == "scan":
            self.attacker_resources -= 5
            # Slight stealth cost from scanning
            self.attacker_stealth -= random.randint(2, 5)
            
        elif action == "exploit":
            target = attacker_action.get("target", "web_server")
            if target in self.systems:
                success_chance = 0.5 + (self.attacker_stealth / 200)  # Higher stealth = better chance
                if random.random() < success_chance:
                    damage = random.randint(20, 40)
                    self.systems[target].take_damage(damage)
                    self.attacker_resources -= 20
                    self.attacker_stealth -= 25  # Risky action
                    self.attacker_score += 10 * (damage // 10)
                else:
                    self.attacker_stealth -= 35  # Got caught trying
                    self.defender_resources += 10  # Defender gains resources from detection
                    
        elif action == "hide":
            self.attacker_stealth = min(100, self.attacker_stealth + 15)
            self.attacker_resources -= 5
            
        elif action == "brute_force":
            target = attacker_action.get("target", "firewall")
            if target in self.systems and not self.systems[target].is_breached:
                self.systems[target].take_damage(50)
                self.attacker_stealth -= 50  # Very risky
                self.attacker_resources -= 30
                self.attacker_score += 20
        
        # Regenerate resources slowly
        self.attacker_resources = min(100, self.attacker_resources + 5)
        self.defender_resources = min(100, self.defender_resources + 5)
        self.attacker_stealth = max(0, self.attacker_stealth - 1)  # Passive detection
        
        # Record turn
        breached_count = sum(1 for s in self.systems.values() if s.is_breached)
        self.history.append({
            "turn": self.turn,
            "attacker_action": action,
            "attacker_target": attacker_action.get("target", "unknown"),
            "defender_action": defender_action.get("action", "monitor"),
            "defender_target": defender_action.get("target", "unknown"),
            "stealth": self.attacker_stealth,
            "systems_breached": breached_count,
            "systems_state": {name: s.security for name, s in self.systems.items()}
        })
        
        self.turn += 1

    def is_game_over(self) -> bool:
        """Check if game is over"""
        all_breached = all(s.is_breached for s in self.systems.values())
        all_secure = all(s.security > 90 for s in self.systems.values())
        
        return (
            all_breached or  # Attacker won
            self.attacker_stealth <= 0 or  # Attacker caught
            self.attacker_resources <= 0 or  # Attacker out of resources
            self.turn > MAX_TURNS  # Time limit
        )
    
    def get_winner(self) -> str:
        """Determine the winner"""
        all_breached = all(s.is_breached for s in self.systems.values())
        
        if all_breached:
            return "attacker"
        elif self.attacker_stealth <= 0:
            return "defender"
        elif self.attacker_resources <= 0:
            return "defender"
        else:
            return "draw"