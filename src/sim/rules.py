import numpy as np
from src.core.agent import Agent

def collision_rule(agent_a: Agent, agent_b: Agent):
    # print(f"Agent {agent_a.get_id()} collided with agent {agent_b.get_id()} ")
    if agent_a.get_hp() == agent_b.get_hp():
        agent_a.update_hp(-1)
        agent_b.update_hp(-1)
    elif agent_a.get_hp() < agent_b.get_hp():
        agent_a.update_hp(-2)
        agent_b.update_hp(-1)
    else:
        agent_a.update_hp(-1)
        agent_b.update_hp(-2)

    # print(f"Outcome:\n{agent_a}\n{agent_b}")