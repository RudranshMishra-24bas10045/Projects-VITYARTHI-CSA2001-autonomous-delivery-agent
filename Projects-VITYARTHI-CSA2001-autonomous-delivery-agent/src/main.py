import argparse, os
from src.env import Env
from src.agent import Agent

def main():
    p = argparse.ArgumentParser()
    p.add_argument("scenario", choices=['static', 'dynamic', 'replan'])
    p.add_argument("--map", default="medium", choices=['small', 'medium', 'large'])
    p.add_argument("--fuel", type=int, default=150)
    args = p.parse_args()

    if args.scenario == 'static':
        env = Env(f'maps/{args.map}.txt')
        agent = Agent(env, fuel=args.fuel)
        agent.plan()
        
    elif args.scenario == 'dynamic':
        env = Env('maps/dynamic_map.txt', sf='maps/dynamic_schedule.json')
        agent = Agent(env, fuel=args.fuel)
        plan = agent.plan()
        if plan: agent.run()

    elif args.scenario == 'replan':
        env = Env('maps/dynamic_map.txt')
        agent = Agent(env, fuel=args.fuel)
        plan = agent.plan()
        if plan:
            path = plan[0]
            block_t = 5
            block_pos = path[block_t] if len(path) > block_t else None
            if block_pos:
                 agent.run(block_t=block_t, block_pos=block_pos)
            else:
                 agent.run()

if __name__ == "__main__":
    main()