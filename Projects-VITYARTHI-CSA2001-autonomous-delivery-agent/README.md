# Autonomous Agent Navigation

## Overview
Implementation of a delivery agent for CSA2001. The agent navigates a 2D grid with static, dynamic, and unforeseen obstacles. The core planner is a time-aware A* search.

## Features
- Environment model for static and dynamic obstacles.
- Time-aware A* planner with Manhattan distance heuristic.
- Fuel constraint handling.
- Local search for dynamic replanning against unforeseen events.

## Setup
Project uses standard Python 3 libraries. No external dependencies required.
Clone the repository: `git clone <your_repo_url>`

## Usage
Execute `main.py` from the root directory to run scenarios.

**1. Static Analysis**
Analyzes a static map with the A* planner.
`python -m src.main static --map medium --fuel 150`
`python -m src.main static --map large --fuel 500`

**2. Dynamic Scenario**
Runs a full mission with scheduled moving obstacles.
`python -m src.main dynamic --fuel 150`

**3. Replanning Demo**
Simulates an unforeseen obstacle, triggering local search replanning.
`python -m src.main replan --fuel 150`