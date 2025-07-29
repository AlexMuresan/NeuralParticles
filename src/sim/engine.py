import numpy as np
from src.core.agent import Agent
from src.core.grid import Grid
from src.sim.rules import collision_rule


class Engine:
    def __init__(self, num_agents: int, grid_size: tuple[int, int]):
        self.num_agents = num_agents
        self.grid = Grid(height=grid_size[0], width=grid_size[1])
        self.agents: dict[int, Agent] = {}
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

    def simulate_step(self) -> list[tuple[int, int]]:
        flash_cells: list[tuple[int, int]] = []
        target2id: dict[tuple[int, int], list[int]] = {}

        for agent_id, agent in self.agents.items():
            dx, dy = agent.propose_movement()
            if dx == 0 and dy == 0:
                continue

            ox, oy = self.grid._wrap(*agent.get_position())
            nx = ox + dx
            ny = oy + dy

            nx, ny = self.grid._wrap(nx, ny)

            if (nx, ny) not in target2id:
                target2id[(nx, ny)] = [agent_id]
            else:
                if agent_id not in target2id[(nx, ny)]:
                    target2id[(nx, ny)].append(agent_id)

        for target_cell, aid_list in target2id.items():
            target_cell_occupant = self.grid.check_position(target_cell)
            if len(aid_list) == 1 and target_cell_occupant == 0:
                aid = aid_list[0]
                ag = self.agents[aid]

                success, (nx, ny) = self.grid.move_with_position(
                    agent_id=aid, old=ag.get_position(), new=target_cell
                )

                if success:
                    ag.update_position((nx, ny))
                else:
                    agent_a_id = aid
                    agent_b_id = self.grid.check_position((nx, ny))
                    if agent_b_id != 0:
                        agent_a = self.agents[agent_a_id]
                        agent_b = self.agents[agent_b_id]
                        collision_rule(agent_a, agent_b)
                    print(f"Unexpected collision when moving agent {aid} to ({nx},{ny})")
            else:
                colliding_agents_id_list = set(aid_list)
                if target_cell_occupant != 0:
                    colliding_agents_id_list.add(target_cell_occupant)

                colliding_agents_id_list = list(set(colliding_agents_id_list))

                for i, agent_a_id in enumerate(colliding_agents_id_list):
                    for j, agent_b_id in enumerate(colliding_agents_id_list):
                        if i < j:
                            if agent_a_id != agent_b_id:
                                agent_a = self.agents[agent_a_id]
                                agent_b = self.agents[agent_b_id]
                                collision_rule(agent_a, agent_b)
                flash_cells.append(target_cell)

        dead = [aid for aid, ag in self.agents.items() if ag.hp <= 0]
        for aid in dead:
            x, y = self.agents[aid].get_position()
            self.grid.positions[x, y] = 0
            del self.agents[aid]

        # assert len(self.agents) == np.count_nonzero(self.grid.positions)

        flash_cells = list(set(flash_cells))
        return flash_cells

    def get_agents(self) -> list[Agent]:
        return list(self.agents.values())

    def get_agent_neighbors(self, agent_id: int):
        agent = self.agents[agent_id]
        return self.grid.neighborhood(coords=agent.get_position())

    def get_agent_positions(self) -> np.ndarray:
        return self.grid.positions
