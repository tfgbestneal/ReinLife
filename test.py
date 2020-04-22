from TheGame import Environment
from TheGame.Models import DQN, D3QN, DDQN, PERD3QN, DRQN, PPO, PERDQN

# main_brains = [PERDQN(152, 8, load_model="Brains/PERDQN/model_40000_881.pt"),  # <-- CURRENTLY BEST BRAIN!!!
#                DQN(152, load_model="Brains/DQN/model_40000_881.pt"),           # <-- CURRENTLY BEST BRAIN!!!
#                D3QN(152, 8, load_model="Brains/D3QN/model_60000_100.pt")]      # <-- CURRENTLY BEST BRAIN!!!

main_brains = [PERD3QN(153, 8, load_model="Experiments/2020-04-22_V8/PERD3QN/brain_1.pt", training=False),
               PERD3QN(153, 8, load_model="Experiments/2020-04-22_V8/PERD3QN/brain_2.pt", training=False)]

env = Environment(width=30, height=30, grid_size=24, evolution=True, max_agents=150,
                  pastel=False, brains=main_brains, training=False, families=True)
s = env.reset()

while True:
    for agent in env.agents:
        if env.brains[agent.gen].method in ["DQN", "D3QN", "PERD3QN"]:
            agent.action = agent.brain.get_action(agent.state, 0)
        elif env.brains[agent.gen].method in ["PPO", "PERDQN"]:
            agent.action = agent.brain.get_action(agent.state)
    env.step()
    s = env.update_env()
    env.render(fps=10)