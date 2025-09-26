import matplotlib.pyplot as plt, matplotlib.animation as animation, numpy as np

class Sim:
    def __init__(self, env, agent_path, dyn_obs_paths):
        self.env, self.agent_path, self.dyn_obs_paths = env, agent_path, dyn_obs_paths
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.agent_marker, self.obs_markers = None, []

    def _setup(self):
        grid = np.zeros((self.env.h, self.env.w))
        for r in range(self.env.h):
            for c in range(self.env.w):
                grid[r, c] = -1 if self.env.grid[r][c] == 1 else self.env.get_cost((r,c))
        self.ax.matshow(grid, cmap='Greys_r')
        sr, sc = self.env.start
        gr, gc = self.env.goal
        self.ax.scatter(sc, sr, marker='o', color='lime', s=150, zorder=5)
        self.ax.scatter(gc, gr, marker='*', color='red', s=250, zorder=5)
        self.ax.set_xticks([]); self.ax.set_yticks([])

    def _animate(self, t):
        agent_pos = self.agent_path[min(t, len(self.agent_path)-1)]
        if self.agent_marker: self.agent_marker.set_offsets(np.c_[agent_pos[1], agent_pos[0]])
        else: self.agent_marker = self.ax.scatter(agent_pos[1], agent_pos[0], marker='o', color='deepskyblue', s=150, zorder=10)
        
        for i, obs_id in enumerate(self.dyn_obs_paths):
            obs_path = self.dyn_obs_paths[obs_id]
            obs_pos = obs_path[min(t, len(obs_path)-1)]
            if i < len(self.obs_markers): self.obs_markers[i].set_offsets(np.c_[obs_pos[1], obs_pos[0]])
            else: self.obs_markers.append(self.ax.scatter(obs_pos[1], obs_pos[0], marker='s', color='orange', s=150, zorder=8))
        
        self.ax.set_title(f'Time: {t}')
        return [self.agent_marker] + self.obs_markers

    def run(self, fname='sim.gif'):
        print(f"Creating sim: {fname}")
        self._setup()
        max_len = len(self.agent_path)
        for obs_id in self.dyn_obs_paths: max_len = max(max_len, len(self.dyn_obs_paths[obs_id]))
        ani = animation.FuncAnimation(self.fig, self._animate, frames=max_len, interval=200, blit=True, repeat=False)
        ani.save(fname, writer='pillow')
        print("Sim saved.")
