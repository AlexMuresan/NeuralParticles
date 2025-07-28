import numpy as np
from typing import List, Tuple, Sequence, Optional


class Grid:
    """
    Defines a grid that keeps track of agent positions.
    Positions are specified using [X, Y] coordinates
        - X=height(row) and
        - Y=width(column)
    """

    def __init__(self, height: int, width: int):
        """
        self.grid     : np.int8   occupancy (0=empty, 1,2,3=species)
        """
        self.width = width
        self.height = height
        self.positions = np.zeros((height, width), dtype=int)

    def _wrap(self, x: int, y: int) -> Tuple[int, int]:
        return x % self.height, y % self.width

    def add(self, agent_id: int, coords: Tuple[int, int]) -> Tuple[int, int]:
        x = int(np.round(coords[0]))
        y = int(np.round(coords[1]))

        x, y = self._wrap(x, y)

        if self.positions[x, y] == 0:
            self.positions[x, y] = agent_id

        return x, y

    def check_position(self, coords) -> int:
        x, y = self._wrap(*coords)
        return self.positions[x, y]

    def move(
        self, agent_id: int, old: tuple[int, int], delta: tuple[int, int]
    ) -> tuple[bool, tuple[int, int]]:

        ox, oy = self._wrap(*old)
        nx, ny = self._wrap(ox + delta[0], oy + delta[1])

        if self.positions[nx, ny] == 0:
            self.positions[ox, oy] = 0
            self.positions[nx, ny] = agent_id

            return True, (nx, ny)
        else:
            return False, (nx, ny)

    def move_with_position(
        self, agent_id: int, old: tuple[int, int], new: tuple[int, int]
    ):
        nx, ny = self._wrap(*new)
        ox, oy = self._wrap(*old)

        if self.positions[nx, ny] == 0:
            self.positions[ox, oy] = 0
            self.positions[nx, ny] = agent_id
            return True, (nx, ny)
        else:
            return False, (nx, ny)

    def neighborhood(self, coords: Tuple[int, int], radius: int = 1) -> List[int]:
        neighbors: list[int] = []

        x = coords[0]
        y = coords[1]

        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx == 0 and dy == 0:
                    continue

                nx, ny = self._wrap(x + dx, y + dy)
                if (aid := self.positions[nx, ny]) != 0:
                    neighbors.append(aid)

        return neighbors
