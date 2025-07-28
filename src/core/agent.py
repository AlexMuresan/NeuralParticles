import numpy as np
from typing import List, Tuple, Sequence, Optional


class Agent:
    def __init__(
        self, id: int, coords: Tuple[int, int], species: int, hp: float
    ) -> None:
        self.x = coords[0]
        self.y = coords[1]

        self.id = id
        self.species = species
        self.hp = hp

    def __str__(self):
        return f"Agent {self.id}:\n\tspecies: {self.species}\n\thp: {self.hp}\n\tpos: ({self.x}, {self.y})"

    def get_id(self) -> int:
        return self.id

    def get_species(self) -> int:
        return self.species

    def get_hp(self) -> float:
        return self.hp

    def get_position(self) -> Tuple[int, int]:
        return self.x, self.y

    def update_hp(self, new_hp: float) -> bool:
        self.hp += new_hp

        if self.hp <= 0:
            return False
        else:
            return True

    def update_position(self, new_coords: Tuple[int, int]):
        self.x = new_coords[0]
        self.y = new_coords[1]
