from src.sim.engine import Engine

if __name__ == "__main__":
    eng = Engine(num_agents=10, grid_size=(11, 11))
    eng.spawn_agents()

    print(eng.get_agent_positions())
    agents = eng.get_agents()
    # for agent in agents:
    #     print(agent)

    for agent in agents:
        if len(eng.get_agent_neighbors(agent.get_id())) != 0:
            print(agent)
            print(eng.get_agent_neighbors(agent.get_id()))