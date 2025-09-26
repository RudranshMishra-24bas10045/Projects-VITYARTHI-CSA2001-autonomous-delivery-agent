import time, heapq, random

def ucs(env, sp, fuel):
    st = time.time()
    q = [(0, sp, [sp])]  
    visited = set()
    exp_nodes = 0

    while q:
        gc, pos, path = heapq.heappop(q)
        exp_nodes += 1

        if pos == env.goal:
            return path, gc, exp_nodes, (time.time() - st) * 1000

        if pos in visited:
            continue
        visited.add(pos)

        
        for n_pos in env.get_neighbors(pos):
            if not env.is_obs(n_pos, 0):
                mc = env.get_cost(n_pos)
                ngc = gc + mc
                if ngc <= fuel and n_pos not in visited:
                    heapq.heappush(q, (ngc, n_pos, path + [n_pos]))
    
    return None, 0, exp_nodes, (time.time() - st) * 1000

def astar(env, sp, fuel):
    st = time.time()
    h = lambda p: abs(p[0] - env.goal[0]) + abs(p[1] - env.goal[1])
    q = [(h(sp), 0, sp, 0, [sp])]
    visited = set()
    exp_nodes = 0
    while q:
        _, gc, pos, t, path = heapq.heappop(q)
        exp_nodes += 1
        if pos == env.goal: return path, gc, exp_nodes, (time.time() - st) * 1000
        if (pos, t) in visited: continue
        visited.add((pos, t))
        nt = t + 1
        for n_pos in env.get_neighbors(pos):
            if not env.is_obs(n_pos, nt) and not env.is_obs(pos, nt):
                mc = env.get_cost(n_pos)
                ngc = gc + mc
                if ngc <= fuel and (n_pos, nt) not in visited:
                    fc = ngc + h(n_pos)
                    heapq.heappush(q, (fc, ngc, n_pos, nt, path + [n_pos]))
    return None, 0, exp_nodes, (time.time() - st) * 1000

def local_search(env, sp, old_path, fuel):
    rejoin_tgt = next((p for p in reversed(old_path) if not env.is_obs(p, 0)), None)
    if not rejoin_tgt: return None
    path = [sp]
    for _ in range(25):
        if path[-1] == rejoin_tgt: break
        ngh = [n for n in env.get_neighbors(path[-1]) if not env.is_obs(n, 0)]
        if not ngh: return None
        path.append(random.choice(ngh))
    if path[-1] == rejoin_tgt:
        cost = sum(env.get_cost(p) for p in path[1:])
        if cost <= fuel: return path
    return None
