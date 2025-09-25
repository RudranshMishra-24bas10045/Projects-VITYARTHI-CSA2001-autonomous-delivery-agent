from src.planner import astar, local_search

class Agent:
    def __init__(self, env, fuel=100):
        self.env = env
        self.fuel = fuel
        self.pos = env.start
        self.path = []
        self.t = 0
        self.total_cost = 0

    def plan(self):
        print("Planning path...")
        res = astar(self.env, self.pos, self.fuel)
        if res[0]:
            self.path = res[0]
            print(f"Plan OK. Cost: {res[1]}, Nodes: {res[2]}")
            return res
        print("Plan failed.")
        return None

    def run(self, block_t=None, block_pos=None):
        if not self.path: return
        while self.pos != self.env.goal and self.t < len(self.path) - 1:
            if self.t == block_t:
                print(f"\nEVENT @ T={self.t}: Obstacle at {block_pos}")
                self.env.grid[block_pos[0]][block_pos[1]] = 1
                if self.path[self.t + 1] == block_pos:
                    print(f"LOG: Path blocked. Replanning.")
                    patch = local_search(self.env, self.pos, self.path[self.t+1:], self.fuel)
                    if patch:
                        print(f"Local search OK. New patch: {patch[1:]}")
                        self.path = self.path[:self.t+1] + patch[1:]
                    else:
                        print("Local search failed. Full replan needed.")
                        res = self.plan()
                        if not res: print("FATAL: Replan failed."); return
            
            self.t += 1
            next_pos = self.path[self.t]
            mc = self.env.get_cost(next_pos)
            if self.fuel >= mc:
                self.fuel -= mc
                self.total_cost += mc
                self.pos = next_pos
                print(f"T={self.t}: pos={self.pos}, cost={mc}, fuel={self.fuel}")
            else:
                print(f"FATAL: Out of fuel."); return
        
        if self.pos == self.env.goal: print("\nSUCCESS: Goal reached.")
        else: print("\nFAIL: Did not reach goal.")