import numpy as np
from typing import List, Tuple, Dict
from src.core.agent import Agent
from src.core.grid import Grid


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

    def get_agents(self) -> List[Agent]:
        return list(self.agents.values())

    def get_agent_neighbors(self, agent_id: int):
        agent = self.agents[agent_id]
        return self.grid.neighborhood(coords=agent.get_position())

    def get_agent_positions(self) -> np.ndarray:
        return self.grid.positions
