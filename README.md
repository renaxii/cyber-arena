# ⚔️ CYBER ARENA

A competitive AI simulation where multiple AI agents battle in cyber attack and defense scenarios.

## 🎮 Game Overview

Cyber Arena is an interactive turn-based strategy game where:
- **Attackers** compete to breach multiple systems on a target network
- **Defenders** work to detect and stop attackers before systems are compromised
- Multiple **AI agents** with different strategies compete against each other
- A **tournament system** allows all agents to compete in a round-robin format

## 🤖 AI Agents

### Attackers (4 Strategies)
1. **Gemini-Smart** - Uses AI model for strategic planning (Google Gemini 2.5 Flash)
2. **Aggressive-Bot** - Prioritizes maximum damage over stealth
3. **Stealth-Ninja** - Focuses on staying hidden while making slow progress
4. **Chaos-Agent** - Random unpredictable behavior

### Defenders (3 Strategies)
1. **Defender-Smart** - Uses AI model for adaptive defense (Google Gemini 2.5 Flash)
2. **Reactive-Guard** - Focuses on repairing most damaged systems
3. **Hunter-Bot** - Prioritizes attack detection and response

## 🕹️ Gameplay Mechanics

### Game State
- **Attacker Stealth**: 0-100 (caught at 0, higher = harder to detect)
- **Attacker Resources**: 0-100 (limits actions per turn)
- **Defender Resources**: 0-100 (limits actions per turn)
- **Target Systems** (3 systems, each with 0-120 security):
  - Web Server (80 security)
  - Database (120 security)
  - Firewall (100 security)

### Attacker Actions
| Action | Cost | Effect | Risk |
|--------|------|--------|------|
| **Scan** | 5 resources | Reveals system info | Low |
| **Exploit** | 20 resources | Damage 20-40 to target | Medium |
| **Brute Force** | 30 resources | Damage 50 to target | High |
| **Hide** | 5 resources | Restore 15 stealth | Low |

### Defender Actions
| Action | Cost | Effect |
|--------|------|--------|
| **Patch** | 15 resources | Restore 25 security to target system |
| **Monitor** | 5 resources | Reduce attacker stealth by 10-20 |
| **Restore** | 25 resources | Massive stealth hit if breached system detected |

### Win Conditions
- **Attacker Wins**: All 3 systems are breached
- **Defender Wins**: Attacker stealth reaches 0 OR attacker runs out of resources
- **Draw**: Reach turn limit (15 turns max)

## 🌐 Web Interface

Access the game at: **http://localhost:8000**

### Features
- **🏠 Home**: Quick stats and leaderboard preview
- **🎮 Play Match**: Watch two selected AI agents compete
- **🏆 Tournament**: Run full round-robin tournament (all attackers vs all defenders)
- **📊 Results**: View complete match history

## 🚀 Getting Started

### Installation
```bash
# Install dependencies
pip install fastapi uvicorn openrouter python-dotenv

# Set up API key
# Create a .env file with your HackClub API key:
# HACKCLUB_API_KEY=your_key_here
```

### Running the Game
```bash
# Start the server
python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000

# Open browser
# Visit: http://localhost:8000
```

## 📊 Leaderboard

Agents earn points:
- **3 points** for winning a match
- **1 point** for a draw

The leaderboard tracks total points across all matches.

## 🏗️ Project Structure

```
cyber-arena/
├── app.py              # FastAPI backend with API endpoints
├── simulation.py       # Game logic and GameState class
├── agents.py           # AI agent classes and strategies
├── static/
│   └── index.html      # Frontend UI
└── README.md
```

## 🔧 Extending the Game

### Add a New Attacker
```python
class MyAttacker(AIAttacker):
    def __init__(self):
        super().__init__("MyAttacker", "model/name", "strategy_name")
    
    def choose_action(self, game_state) -> dict:
        # Your strategy here
        return {"action": "scan", "target": "web_server"}

# Add to ATTACKERS list in agents.py
ATTACKERS.append(MyAttacker())
```

### Add a New Defender
```python
class MyDefender(AIDefender):
    def __init__(self):
        super().__init__("MyDefender", "model/name", "strategy_name")
    
    def choose_action(self, game_state) -> dict:
        # Your strategy here
        return {"action": "monitor", "target": "firewall"}

# Add to DEFENDERS list in agents.py
DEFENDERS.append(MyDefender())
```

## 📈 Example Match Flow

```
Turn 1:
  Attacker (Stealth: 100) → Scan web_server
  Defender (Resources: 100) → Patch firewall
  Result: Web Server: 75 security | Attacker Stealth: 97

Turn 2:
  Attacker (Stealth: 97) → Exploit database
  Defender (Resources: 85) → Monitor network
  Result: Database: 85 security | Attacker Stealth: 71
```

## 🎯 Strategy Tips

### For Attackers:
- **Aggressive**: Exploit heavily guarded systems for big damage
- **Stealth**: Use hiding to maintain detection avoidance
- **Balanced**: Mix scanning with strategic exploits

### For Defenders:
- **Proactive**: Patch systems before they're damaged
- **Reactive**: Monitor to detect attacks early
- **Aggressive**: Counter-attack when attacker is detected

## 📝 License

This project is part of HackClub cyber security education.

## 🙌 Credits

Built with:
- FastAPI (backend)
- TailwindCSS (frontend)
- OpenRouter (AI API access)
- Uvicorn (ASGI server)
