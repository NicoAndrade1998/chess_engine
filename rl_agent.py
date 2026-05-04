import numpy as np
import torch
import random

from collections import deque

# ----------------------------
# REPLAY BUFFER
# ----------------------------
class ReplayBuffer:
    def __init__(self, size=50000):
        self.buffer = deque(maxlen=size)

    def add(self, s, a, r, s2, done):
        self.buffer.append((s, a, r, s2, done))

    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        s, a, r, s2, d = map(list, zip(*batch))
        return s, a, r, s2, d

    def __len__(self):
        return len(self.buffer)


# ----------------------------
# ACTION SELECTION
# ----------------------------
def select_action(model, state, legal_moves, epsilon):
    if np.random.rand() < epsilon:
        return random.choice(legal_moves)

    state_t = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
    q_values = model(state_t).detach().numpy()[0]

    legal_actions = [encode_move(m) for m in legal_moves]

    best_action = max(legal_actions, key=lambda a: q_values[a])

    return decode_move(best_action)


# ----------------------------
# TRAINING LOOP
# ----------------------------
def train(env, model, optimizer, episodes=1000):

    buffer = ReplayBuffer()

    gamma = 0.99
    epsilon = 1.0
    epsilon_decay = 0.995
    epsilon_min = 0.1
    batch_size = 64

    for episode in range(episodes):

        state = env.reset()
        done = False
        total_reward = 0

        while not done:

            legal_moves = env.get_legal_moves()

            if len(legal_moves) == 0:
                break

            action = select_action(model, state, legal_moves, epsilon)

            next_state, reward, done = env.step(action)

            buffer.add(state, encode_move(action), reward, next_state, done)

            state = next_state
            total_reward += reward

            # ----------------------------
            # LEARNING STEP
            # ----------------------------
            if len(buffer) > batch_size:

                s, a, r, s2, d = buffer.sample(batch_size)

                s = torch.tensor(np.array(s), dtype=torch.float32)
                s2 = torch.tensor(np.array(s2), dtype=torch.float32)
                a = torch.tensor(a)
                r = torch.tensor(r, dtype=torch.float32)
                d = torch.tensor(d, dtype=torch.float32)

                q_values = model(s)

                next_q = model(s2).max(dim=1)[0].detach()

                target = r + gamma * next_q * (1 - d)

                q_pred = q_values.gather(1, a.unsqueeze(1)).squeeze()

                loss = torch.nn.functional.mse_loss(q_pred, target)

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

        epsilon = max(epsilon_min, epsilon * epsilon_decay)

        print(f"Episode {episode} | Reward: {total_reward:.3f} | Epsilon: {epsilon:.3f}")


# ----------------------------
# MAIN (RUN TRAINING)
# ----------------------------
if __name__ == "__main__":

    env = ChessEnv()
    model = DQN()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

    train(env, model, optimizer)