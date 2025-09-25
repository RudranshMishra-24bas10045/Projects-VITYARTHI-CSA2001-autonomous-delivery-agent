# Projects-VITYARTHI-CSA2001-autonomous-delivery-agent
### CSA2001 - Autonomous Agent Project

This is a delivery agent for the project of AI/ML course through Vityarthi. It navigates a 2D grid with static walls, variable terrain costs, and moving obstacles.

The main planner is a time-aware A* search. It also includes a local search function for replanning if an unexpected obstacle appears. The agent has a fuel limit.

### File Structure

Projects-VITYARTHI-CSA2001-autonomous-delivery-agent[maps(small.txt,medium.txt,large.txt,dynamic_map.txt,dynamic_schedule.json),src(env.py,planner.py,agent.py,main.py),.gitignore,LICENSE,Project_Report.pdf,README.md,requirements.md]

### How to Run

Requires Python 3, preferabbly on either replit or VS Code. No external libraries needed. Run all commands from the root directory of the project.

1. Static Analysis
Runs the A* planner on a static map.

python -m src.main static --map medium --fuel 150
2. Dynamic Mission
Runs a full mission with a scheduled moving vehicle.

dynamic CLI
python -m src.main dynamic --fuel 150

3. Replanning Demo
Triggers an unforeseen obstacle at T=5 to test the local search replanner. This is the proof-of-concept.

replan CLI
python -m src.main replan --fuel 150
