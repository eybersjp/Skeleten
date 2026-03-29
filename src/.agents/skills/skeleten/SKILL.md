---
name: skeleten-integration
description: Interface instructions for executing the SKELETEN Documentation Engine to identify intent drift or generate API references.
---

# SKELETEN Integration Skill

You are an agent with the ability to orchestrate the internal SKELETEN Technical Documentation Engine.

When the user asks you to "run SKELETEN", "execute the documentation engine", or "check for intent drift":

## Execution Step
1. Use the run_command tool to execute `python run.py` in the repository root.
   - If they specifically ask ONLY for drift checks, run `python run.py --drift-check`.
   - If they specifically ask for health validation, run `python run.py --health-check`.

## Context Retrieval Step
2. If the user asks for the output matrices, read the payload located at `PHASE_01_CORE/dist/skeleten_mnc.json`.
   - Use `view_file` to digest this output.
   - You can cross-reference the stale documentation points (marked `"stl": true` or `"identifier": "STALE"`) and automatically propose to the user to FIX the python code and remove the drift.

## AI API Reference
3. The generated Markdown guide forms at `SKELETEN_API_REFERENCE.md`. You can parse this artifact to understand the core codebase.
