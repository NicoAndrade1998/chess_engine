from chess_env import ChessEnv
from ppo_agent import PPOAgent
from utils import decode_move

env = ChessEnv()
agent = PPOAgent()

state = env.reset()
done = False

total_reward = 0
steps = 0

while not done and steps < 50:

    action, log_prob, value = agent.select_action(state, env)
    move = decode_move(action)

    state, reward, done = env.step(move)

    total_reward += reward
    steps += 1

print("Episode finished")
print("Steps:", steps)
print("Total reward:", total_reward)