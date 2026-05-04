import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from utils import encode_move, decode_move


# -------------------------
# ACTOR-CRITIC NETWORK
# -------------------------
class ActorCritic(nn.Module):
    def __init__(self):
        super().__init__()

        self.conv = nn.Sequential(
            nn.Conv2d(12, 64, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, 128, 3, padding=1),
            nn.ReLU(),
        )

        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(8 * 8 * 128, 512),
            nn.ReLU()
        )

        self.policy_head = nn.Linear(512, 4096)
        self.value_head = nn.Linear(512, 1)

    def forward(self, x):
        x = self.conv(x)
        x = self.fc(x)

        return self.policy_head(x), self.value_head(x)


# -------------------------
# PPO AGENT
# -------------------------
class PPOAgent:
    def __init__(self):
        self.model = ActorCritic()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=3e-4)

        self.memory = []

    # board → tensor
    def preprocess(self, board):
        t = torch.tensor(board, dtype=torch.float32)
        return t.permute(2, 0, 1).unsqueeze(0)

    # -------------------------
    # MASK LEGAL MOVES
    # -------------------------
    def get_mask(self, env):
        mask = np.zeros(4096, dtype=np.float32)

        for move in env.get_legal_moves():
            mask[encode_move(move)] = 1.0

        return mask

    # -------------------------
    # ACTION SELECTION
    # -------------------------
    def select_action(env, model, state):
        state_t = torch.tensor(state, dtype=torch.float32).unsqueeze(0)

        logits, value = model(state_t)
        logits = logits.squeeze(0)

        legal_moves = env.get_legal_moves()
        legal_indices = [encode_move(m) for m in legal_moves]

        mask = torch.zeros_like(logits)
        mask[legal_indices] = 1.0


        masked_logits = logits + (mask + 1e-8).log()

        probs = torch.softmax(masked_logits, dim=-1)

        dist = torch.distributions.Categorical(probs)
        action_idx = dist.sample()

        log_prob = dist.log_prob(action_idx)

        move = decode_move(action_idx.item())

        return move, action_idx, log_prob, value.squeeze(0), mask

    # store transitions
    def store(self, transition):
        self.memory.append(transition)


    # -------------------------
    # PPO UPDATE
    # -------------------------
    def update(self, gamma=0.99, eps=0.2, entropy_coef=0.01):

        states, actions, rewards, log_probs, values, masks = zip(*self.memory)

        states = list(states)
        actions = torch.tensor(actions, dtype=torch.long)
        old_log_probs = torch.tensor(log_probs, dtype=torch.float32)
        values = torch.tensor(values, dtype=torch.float32)

        # -------------------------
        # Compute returns
        # -------------------------
        returns = []
        G = 0
        for r in reversed(rewards):
            G = r + gamma * G
            returns.insert(0, G)

        returns = torch.tensor(returns, dtype=torch.float32)

        # -------------------------
        # ADVANTAGES
        # -------------------------
        advantages = returns - values
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

        # -------------------------
        # PPO TRAINING
        # -------------------------
        for _ in range(6):

            for i in range(len(states)):
                state = self.preprocess(states[i])
                action = actions[i]
                old_log = old_log_probs[i]
                adv = advantages[i]

                logits, value = self.model(state)
                logits = logits.squeeze(0)

                # ✅ APPLY MASK (CRITICAL)
                mask = torch.tensor(masks[i], dtype=torch.float32)
                masked_logits = logits + (mask + 1e-8).log()

                probs = torch.softmax(masked_logits, dim=0)
                dist = torch.distributions.Categorical(probs)

                new_log = dist.log_prob(action)

                ratio = torch.exp(new_log - old_log)

                # PPO CLIP
                surr1 = ratio * adv
                surr2 = torch.clamp(ratio, 1 - eps, 1 + eps) * adv

                actor_loss = -torch.min(surr1, surr2)

                # critic
                critic_loss = (returns[i] - value.squeeze()) ** 2

                # entropy
                entropy = dist.entropy()

                loss = actor_loss + 0.5 * critic_loss - entropy_coef * entropy

                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

        self.memory = []