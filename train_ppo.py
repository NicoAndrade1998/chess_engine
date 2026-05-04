import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

from chess_env import ChessEnv
from utils import encode_move, decode_move
from model import PPOModel

# -------------------------
# HYPERPARAMETERS
# -------------------------
GAMMA = 0.99
LR = 1e-4
EPS_CLIP = 0.2
K_EPOCHS = 4

device = torch.device("cpu")


# -------------------------
# HELPER: select action
# -------------------------
def select_action(env, model, state):
    state_t = torch.tensor(state, dtype=torch.float32).unsqueeze(0)

    logits, value = model(state_t)

    logits = logits.squeeze(0)

    legal_moves = env.get_legal_moves()
    legal_indices = [encode_move(m) for m in legal_moves]

    mask = torch.zeros(4096)
    mask[legal_indices] = 1

    # mask illegal moves
    masked_logits = logits + (mask - 1) * 1e9

    probs = torch.softmax(masked_logits, dim=-1)

    dist = torch.distributions.Categorical(probs)
    action_idx = dist.sample()

    log_prob = dist.log_prob(action_idx)

    move = decode_move(action_idx.item())

    return move, action_idx, log_prob, value.squeeze(), mask


# -------------------------
# RETURNS + ADVANTAGE
# -------------------------
def compute_returns(rewards, values, dones):
    returns = []
    G = 0

    for r, done in zip(reversed(rewards), reversed(dones)):
        if done:
            G = 0
        G = r + GAMMA * G
        returns.insert(0, G)

    returns = torch.tensor(returns, dtype=torch.float32)
    values = torch.tensor(values, dtype=torch.float32)

    advantages = returns - values
    advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

    return returns, advantages


# -------------------------
# TRAIN LOOP
# -------------------------
def train():
    env = ChessEnv()
    model = PPOModel().to(device)
    optimizer = optim.Adam(model.parameters(), lr=LR)

    for episode in range(1000):

        state = env.reset()

        states = []
        actions = []
        log_probs = []
        rewards = []
        values = []
        dones = []
        masks = []

        # -------- PLAY GAME --------
        while True:

            move, action_idx, log_prob, value, mask = select_action(env, model, state)

            next_state, reward, done = env.step(move)

            states.append(state)
            actions.append(action_idx.item())
            log_probs.append(log_prob.detach())
            rewards.append(reward)
            values.append(value.item())
            dones.append(done)
            masks.append(mask)

            state = next_state

            if done:
                break

        # -------- RETURNS --------
        returns, advantages = compute_returns(rewards, values, dones)

        states = torch.tensor(np.array(states), dtype=torch.float32)
        actions = torch.tensor(actions)
        old_log_probs = torch.stack(log_probs)
        masks = torch.stack(masks)

        # -------- PPO UPDATE --------
        for _ in range(K_EPOCHS):

            logits, state_values = model(states)

            total_loss = 0

            for i in range(len(states)):
                logit = logits[i]
                mask = masks[i]

                masked_logits = logit + (mask - 1) * 1e9

                probs = torch.softmax(masked_logits, dim=-1)
                dist = torch.distributions.Categorical(probs)

                new_log_prob = dist.log_prob(actions[i])

                ratio = torch.exp(new_log_prob - old_log_probs[i])

                surr1 = ratio * advantages[i]
                surr2 = torch.clamp(ratio, 1 - EPS_CLIP, 1 + EPS_CLIP) * advantages[i]

                policy_loss = -torch.min(surr1, surr2)

                value_loss = (returns[i] - state_values[i].squeeze()) ** 2

                entropy = dist.entropy()

                total_loss += policy_loss + 0.5 * value_loss - 0.01 * entropy

            optimizer.zero_grad()
            total_loss.backward()
            optimizer.step()

        print(f"Episode {episode} | Reward: {sum(rewards):.2f}")

        if episode % 50 == 0:
            torch.save(model.state_dict(), "ppo_chess.pth")


if __name__ == "__main__":
    train()