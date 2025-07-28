# src/vis/renderer.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.colors import ListedColormap


class GridRenderer:
    """
    Simple matplotlib viewer:
    • black  - empty cell
    • white  - live agent
    • red    - cells that just experienced a collision (flash duration configurable)
    """

    def __init__(self, grid, flash_frames: int = 3):
        self.grid         = grid
        self.flash_frames = flash_frames
        self.flash_map    = np.zeros_like(grid.positions, dtype=np.uint8)  # 0 = no flash, >0 = countdown

        self.cmap = ListedColormap(["black", "white", "red"])

        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.im = self.ax.imshow(
            self._compose_frame(),
            cmap=self.cmap,
            vmin=0, vmax=2,          # three colour indices 0-2
            interpolation="nearest"
        )
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_title("NeuralParticles — live view")

    # ---------- public hook for the engine ----------
    def notify_collision(self, x: int, y: int):
        """Tell the renderer that cell (x,y) should flash red."""
        self.flash_map[x, y] = self.flash_frames

    # ---------- internal helpers ----------
    def _tick_flash(self):
        """Count down flash timers."""
        self.flash_map[self.flash_map > 0] -= 1

    def _compose_frame(self):
        """
        Overlay flash layer (value 2) on top of base layer
        (0 = empty, 1 = agent). 2+1=3 maps to red (index 2 after clipping).
        """
        base = (self.grid.positions > 0).astype(np.uint8)   # 0 or 1
        overlay = (self.flash_map > 0).astype(np.uint8) * 2
        frame = np.clip(base + overlay, 0, 2)
        return frame

    def _frame_func(self, *_):
        self._tick_flash()
        self.im.set_data(self._compose_frame())
        return (self.im,)

    def animate(self, step_callback, interval=150):
        def _update(_frame):
            step_callback()
            self._tick_flash()
            self.im.set_data(self._compose_frame())
            return (self.im,)          # tuple of artists

        # Turn blitting OFF to sidestep the resize callback entirely
        return animation.FuncAnimation(
            self.fig, _update, interval=interval, blit=False
        )
