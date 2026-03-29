---
description: Run the SKELETEN Phase 00 Intent Wizard to gather project requirements before coding begins.
---

# /skeleten-wizard

Use this workflow when the user wants to start a new project or define initial architectural intents for an empty repository.

## Steps
1. **Trigger Wizard**: Run `python run.py --wizard` using the `run_command` tool.
2. **Interactive Session**: The agent should notify the user that an interactive session is starting in the terminal.
   - Note: Since the wizard is interactive, the agent might need to handle user inputs if prompted in the terminal, or simply guide the user to the terminal.
3. **Intent Baseline**: Once finished, the agent should read `dist/skeleten_intent.json` and `SKELETEN_DESIGN_SPEC.md` to understand the project's ground truth.
4. **Scaffolding**: The agent can then use the captured intent to suggest or generate initial code structure.
