import json

class Env:
    def __init__(self, mf, sf=None):
        self.grid, self.costs = self._load(mf)
        self.h, self.w = len(self.grid), len(self.grid[0])
        self.start, self.goal = self._find('S'), self._find('G')
        self.dyn_obs = json.load(open(sf)) if sf else {}

    def _load(self, mf):
        g, c = [], {}
        with open(mf, 'r') as f:
            for r, line in enumerate(f.readlines()):
                if not line.strip(): continue
                row = []
                for c_idx, char in enumerate(line.strip().split()):
                    pos = (r, c_idx)
                    if char.isdigit(): row.append(0); c[pos] = int(char)
                    elif char == '#': row.append(1) # Wall
                    elif char == 'S': row.append(2); c[pos] = 1
                    elif char == 'G': row.append(3); c[pos] = 1
                g.append(row)
        return g, c

    def _find(self, char):
        tgt = 2 if char == 'S' else 3
        for r, row in enumerate(self.grid):
            for c_val, cell in enumerate(row):
                if cell == tgt: return (r, c_val)

    def get_cost(self, pos): return self.costs.get(pos, 1)

    def is_obs(self, pos, t):
        r, c = pos
        # This safety check fixes the crash on the large map
        if r >= len(self.grid) or c >= len(self.grid[r]):
            return True # Treat anything out of bounds as an obstacle
    
        if self.grid[r][c] == 1: return True
        for _, sched in self.dyn_obs.items():
            path = sched['path']
            idx = t % len(path) if sched.get('loop') else min(t, len(path) - 1)
            if tuple(path[idx]) == pos: return True
        return False

    def get_neighbors(self, pos):
        r, c = pos
        ngh = []
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            np = (r + dr, c + dc)
            if 0 <= np[0] < self.h and 0 <= np[1] < self.w:
                ngh.append(np)

        return ngh
