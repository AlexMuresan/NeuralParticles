from src.sim.engine import Engine

if __name__ == "__main__":
    eng = Engine(num_agents=10, grid_size=(11, 11))
    eng.spawn_agents()

    print(eng.get_agent_positions())
    agents = eng.get_agents()

    for epoch in range(100):
        eng.simulate_step()
        print(f"Epoch {epoch}: alive = {len(eng.agents)}")

    print(eng.get_agent_positions())
