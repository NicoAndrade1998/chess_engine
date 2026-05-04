import torch
import numpy as np

from chess_env import ChessEnv
from model import DQN
from utils import encode_move, decode_move


# ------------------------
# INIT
# ------------------------
env = ChessEnv()
model = DQN()

state = env.reset()

print("Initial state shape:", state.shape)


# ------------------------
# ONE RANDOM MOVE TEST
# ------------------------
legal_moves = env.get_legal_moves()

print("Legal moves:", len(legal_moves))

if len(legal_moves) == 0:
    print("No legal moves found (error)")
    exit()


# pick random move
move = legal_moves[0]

print("Test move:", move)

encoded = encode_move(move)
decoded = decode_move(encoded)

print("Encoded:", encoded)
print("Decoded:", decoded)


# ------------------------
# ONE STEP TEST
# ------------------------
next_state, reward, done = env.step(move)

print("Next state shape:", next_state.shape)
print("Reward:", reward)
print("Done:", done)


# ------------------------
# MODEL TEST
# ------------------------
state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
output = model(state_tensor)

print("Model output shape:", output.shape)