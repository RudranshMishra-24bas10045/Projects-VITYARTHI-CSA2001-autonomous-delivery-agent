### CSA2001 - Autonomous Delivery Agent Project (Vityarthi)

This repository contains the source code for an autonomous delivery agent.

The agent navigates a 2D grid with static walls, terrain costs, and moving obstacles. The main planner is a time-aware A* search, which is compared against a baseline Uniform-Cost Search. A local search function is included for replanning when an unexpected obstacle appears. Fuel is a constraint.

### Project Files

src/: All python source code.
    env.py: Environment model.
    planner.py: UCS, A*, and local search functions.
    agent.py: Agent logic.
    sim.py: Animation/GIF generator.
    main.py: CLI entry point.
maps/: All map data (`.txt` and `.json` files).
Root Folder: Contains the PDF report, this readme, and `requirements.md`.

---
### How to Run

**1. Setup**
Requires Python 3 prefferablly on VS code or replit. You also need one library for the simulation.

pip install matplotlib


**2. Usage**
Run all commands from the project's root directory in a terminal .

**Static Comparison:**
Runs UCS and A\* on a static map to compare performance.


python -m src.main static --map medium

Instead of medium change it to small,large for testing their ucs vs A*.

**Dynamic Mission:**
Runs a full mission with a scheduled moving vehicle.


python -m src.main dynamic


**Replanning Test:**
Triggers an unforeseen obstacle at T=5 to test the local search. This is the proof-of-concept.


python -m src.main replan


**Generate a Simulation:**
Add the `--sim` flag to *any* of the above commands to create an animated `.gif` of the run.

CLI- replan 
python -m src.main replan --sim

This will create a `replan_sim.gif` file in the main folder.
