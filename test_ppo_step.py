from chess_env import ChessEnv
from ppo_agent import PPOAgent

env = ChessEnv()
agent = PPOAgent()

state = env.reset()

action, log_prob, value = agent.select_action(state, env)

print("Action index:", action)
print("Log prob:", log_prob)
print("Value:", value)

from utils import decode_move
move = decode_move(action)

print("Decoded move:", move)

next_state, reward, done = env.step(move)

print("Reward:", reward)
print("Done:", done)
print("Next state shape:", next_state.shape)