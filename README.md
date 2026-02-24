# cyber arena
Cyber Arena is an interactive AI vs. AI cybersecurity simulation.

Currently, it pits two language models against each other in a turn-based strategy game:
- Gemini 2.5 Flash (Attacker)
- DeepSeek Chat (Defender)

Each model receives the same game state and must choose actions that either compromise or defend a simulated server.

## how it works
- Attacker attempts to reduce server security to 0.
- Defender attempts to detect or stop the attacker.
- The game runs for a maximum of 5 turns.
- Each turn:
  - Both models receive the current state.
  - Both respond with JSON decisions.
  - The engine applies deterministic rules.
