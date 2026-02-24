import random

MAX_TURNS = 5

class GameState:
    def __init__(self):
        self.attacker_stealth = 100
        self.server_security = 100
        self.turn = 1
        self.history = []

    def apply_turn(self, attacker_action, defender_action):
        # Defender
        if defender_action == "patch":
            self.server_security += 10
        elif defender_action == "monitor":
            self.attacker_stealth -= 10

        # Attacker
        if attacker_action == "scan":
            self.server_security -= 5

        elif attacker_action == "exploit":
            success = random.random() > 0.4
            if success:
                self.server_security -= 20
                self.attacker_stealth -= 15
            else:
                self.attacker_stealth -= 25

        elif attacker_action == "hide":
            self.attacker_stealth += 10

        self.history.append({
            "turn": self.turn,
            "attacker_action": attacker_action,
            "defender_action": defender_action,
            "stealth": self.attacker_stealth,
            "security": self.server_security
        })

        self.turn += 1

    def is_game_over(self):
        return (
            self.server_security <= 0 or
            self.attacker_stealth <= 0 or
            self.turn > MAX_TURNS
        )