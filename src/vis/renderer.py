import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from src.sim.engine import Engine


def update(data):
    mat.set_data(data)
    return mat


def yield_step():
    while True:
        eng.simulate_step()
        alive_text.set_text(f"Alive: {len(eng.agents)}")
        yield np.clip(eng.get_agent_positions(), 0, 1)


NUM_AGENTS = 512
GRID_SIZE = (128, 128)
FPS = 24
INTERVAL_MS = int(1000 / FPS)

eng = Engine(num_agents=NUM_AGENTS, grid_size=GRID_SIZE)
eng.spawn_agents()

fig, ax = plt.subplots(figsize=(10, 10))
mat = ax.matshow(
    np.clip(eng.get_agent_positions(), 0, 1), cmap="gray", interpolation="nearest"
)
ax.set_xticks([])
ax.set_yticks([])
ax.set_title("NeuralParticles — live view")
alive_text = ax.text(
    10, 10, f"Alive: {len(eng.agents)}", color="r", fontweight="bold", fontsize=16
)

ani = animation.FuncAnimation(
    fig, update, yield_step, save_count=50, interval=INTERVAL_MS
)
plt.show()
