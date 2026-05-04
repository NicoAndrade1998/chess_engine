from chess_env import ChessEnv
from chess_agent import ChessAgent

env = ChessEnv()
agent = ChessAgent()

episodes = 50

for ep in range(episodes):
    state = env.reset()
    done = False
    total_reward = 0

    while not done:
        action = agent.select_action(state, env)

        state, reward, done = env.step(action)

        total_reward += reward

    print(f"Episode {ep}: reward = {total_reward}")