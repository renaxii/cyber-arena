import random

class GameState:
    def __init__(self):
        self.attacker_stealth = 100
        self.server_security = 100
        self.turn = 1

    def apply_action(self, action):
        if action == "scan":
            self.server_security -= 5
            print("Attacker scans the system (-5 security)")
        elif action == "exploit":
            success = random.random() > 0.4
            if success:
                self.server_security -= 20
                self.attacker_stealth -= 15
                print("Exploit succeeded! (-20 security, -15 stealth)")
            else:
                self.attacker_stealth -= 25
                print("Exploit failed! (-25 stealth)")
        elif action == "hide":
            self.attacker_stealth += 10
            print("Attacker hides (+10 stealth)")

        self.turn += 1

    def is_game_over(self):
        return (
            self.server_security <= 0 or
            self.attacker_stealth <= 0 or
            self.turn > 10
        )

    def print_state(self):
        print(f"\n--- Turn {self.turn} ---")
        print(f"Stealth: {self.attacker_stealth}")
        print(f"Security: {self.server_security}")