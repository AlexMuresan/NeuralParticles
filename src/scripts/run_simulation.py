import matplotlib.pyplot as plt
from src.sim.engine    import Engine
from src.vis.renderer  import GridRenderer

GRID   = (512, 512)
N_AG   = 10000
FPS    = 60               # adjust to taste
INTERVAL_MS = int(1000 / FPS)

if __name__ == "__main__":
    eng = Engine(num_agents=N_AG, grid_size=GRID)
    eng.spawn_agents()

    renderer = GridRenderer(eng.grid, flash_frames=3)

    def advance_one_tick():
        for x, y in eng.step():           # Engine.step() returns collision cells
            renderer.notify_collision(x, y)

    ani = renderer.animate(advance_one_tick, interval=INTERVAL_MS)
    plt.show()
