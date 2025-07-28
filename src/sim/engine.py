import numpy as np
from typing import List, Tuple, Dict, Optional
from src.core.agent import Agent
from src.core.grid import Grid
from src.sim.rules import collision_rule


class Engine:
    def __init__(self, num_agents: int, grid_size: Tuple[int, int]):
        self.num_agents = num_agents
        self.grid = Grid(height=grid_size[0], width=grid_size[1])
        self.agents: Dict[int, Agent] = {}
        self.max_id = 1

        assert (
            self.num_agents <= grid_size[0] * grid_size[1]
        ), f"the number of agents: {self.num_agents} can't be larger than the total grid area: {grid_size[0] * grid_size[1]}"

    def spawn_agents(self):
        for i in range(self.num_agents):
            available_positions = np.where(self.grid.positions == 0)
            tmp_x = np.random.choice(available_positions[0])
            tmp_y = np.random.choice(available_positions[1])

            tmp_agent = Agent(id=self.max_id, coords=(tmp_x, tmp_y), species=1, hp=10)

            self.grid.add(tmp_agent.get_id(), tmp_agent.get_position())
            self.agents[tmp_agent.get_id()] = tmp_agent
            self.max_id += 1

    # def step_move(
    #     self, agent: Agent, delta_movement: tuple[int, int]
    # ) -> Optional[tuple[int, int]]:
    #     success, new_coords = self.grid.move(
    #         agent_id=agent.get_id(), old=agent.get_position(), delta=delta_movement
    #     )
    #     if success:
    #         agent.update_position(new_coords=new_coords)
    #         return None
    #     else:
    #         collided_agent_id = self.grid.check_position(new_coords)
    #         if agent.get_id() != collided_agent_id:
    #             collision_rule(agent_a=agent, agent_b=self.agents[collided_agent_id])
    #             return new_coords
    #         return None

    def step(self) -> list[tuple[int, int]]:
        """Advance one tick, return list of grid coords involved in collisions."""
        # -------- phase 1: everybody chooses -------------
        wants: dict[tuple[int, int], list[int]] = {}          # tgt → [agent ids]
        for ag in self.agents.values():
            dx, dy = np.random.choice([-1, 0, 1], 2)
            if dx == 0 and dy == 0:           # staying put is never a proposal
                continue

            tgt = self.grid._wrap(ag.x + dx, ag.y + dy)
            wants.setdefault(tgt, []).append(ag.id)

        flash: list[tuple[int, int]] = []

        # -------- phase 2: resolve ------------------------
        for tgt, ids in wants.items():
            cell_occupant = self.grid.positions[tgt]

            # Case A – empty cell & exactly one suitor  → move succeeds
            if cell_occupant == 0 and len(ids) == 1:
                aid          = ids[0]
                old          = self.agents[aid].get_position()
                self.grid.move(aid, old, (tgt[0]-old[0], tgt[1]-old[1]))
                self.agents[aid].update_position(tgt)
                continue

            # Case B – anything else → handle collision
            # Gather all parties: the suitors + the current occupant (if any)
            parties = ids.copy()
            if cell_occupant != 0 and cell_occupant not in parties:
                parties.append(cell_occupant)

            # Apply pair‑wise rules (simplest: first vs each other)
            for i in range(len(parties)):
                for j in range(i + 1, len(parties)):
                    collision_rule(self.agents[parties[i]],
                                self.agents[parties[j]])

            flash.append(tgt)                 # tell renderer to flash this cell

        # -------- phase 3: cull the dead ------------------
        dead = [aid for aid, ag in self.agents.items() if ag.hp <= 0]
        for aid in dead:
            x, y = self.agents[aid].get_position()
            self.grid.positions[x, y] = 0
            del self.agents[aid]

        return flash

    # def simulate_step(self):
    #     for agent_id, agent in self.agents.items():
    #         dx, dy = np.random.choice([-1, 0, 1], size=2)
    #         self.step_move(agent, (dx, dy))

    def get_agents(self) -> List[Agent]:
        return list(self.agents.values())

    def get_agent_neighbors(self, agent_id: int):
        agent = self.agents[agent_id]
        return self.grid.neighborhood(coords=agent.get_position())

    def get_agent_positions(self) -> np.ndarray:
        return self.grid.positions
