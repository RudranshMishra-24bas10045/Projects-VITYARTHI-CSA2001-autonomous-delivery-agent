import argparse, os
from src.env import Env
from src.agent import Agent
# This is the fully updated main.py with all features

def main():
    p = argparse.ArgumentParser()
    p.add_argument("scenario", choices=['static', 'dynamic', 'replan'])
    p.add_argument("--map", default="medium", choices=['small', 'medium', 'large'])
    p.add_argument("--fuel", type=int, default=150)
    p.add_argument("--sim", action='store_true', help="Run and save simulation GIF")
    args = p.parse_args()

    agent, env = None, None

    if args.scenario == 'static':
        print(f"--- STATIC comparison: maps/{args.map}.txt ---")
        env = Env(f'maps/{args.map}.txt')
        from src.planner import ucs, astar
        
        print("\nUCS run:")
        ucs_res = ucs(env, env.start, args.fuel)
        if ucs_res[0]: print(f"  Path OK. Cost: {ucs_res[1]}, Nodes: {ucs_res[2]}")
        else: print("  UCS Fail.")
        
        print("\nA* run:")
        astar_res = astar(env, env.start, args.fuel)
        if astar_res[0]: print(f"  Path OK. Cost: {astar_res[1]}, Nodes: {astar_res[2]}")
        else: print("  A* Fail.")
        
        if args.sim and astar_res[0]:
            agent = Agent(env, fuel=args.fuel); agent.path = astar_res[0]; agent.history = agent.path

    elif args.scenario in ['dynamic', 'replan']:
        env = Env('maps/dynamic_map.txt', sf='maps/dynamic_schedule.json' if args.scenario == 'dynamic' else None)
        agent = Agent(env, fuel=args.fuel)
        plan = agent.plan()
        if plan:
            if args.scenario == 'replan':
                path, block_t = plan[0], 5
                block_pos = path[block_t + 1] if len(path) > block_t + 1 else None
                if block_pos: agent.run(block_t=block_t, block_pos=block_pos)
                else: agent.run()
            else:
                agent.run()

    if args.sim and agent and agent.history:
        from src.sim import Sim
        dyn_obs_paths = {}
        if env.dyn_obs:
            max_t = len(agent.history)
            for obs_id, sched in env.dyn_obs.items():
                path = sched['path']
                dyn_obs_paths[obs_id] = [tuple(path[t % len(path) if sched.get('loop') else min(t, len(path)-1)]) for t in range(max_t)]
        
        sim = Sim(env, agent.history, dyn_obs_paths)
        sim.run(fname=f"{args.scenario}_{args.map if args.scenario=='static' else 'sim'}.gif")

if __name__ == "__main__":
    main()
