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
    def select_action(self, state, env):
        state_t = self.preprocess(state)

        logits, value = self.model(state_t)

        logits = logits.detach().squeeze(0)
        value = value.item()

        mask = self.get_mask(env)

        # 🚨 mask illegal moves
        masked_logits = logits + torch.tensor((mask - 1) * 1e9)

        probs = F.softmax(masked_logits, dim=0)

        dist = torch.distributions.Categorical(probs)
        action_idx = dist.sample()

        log_prob = dist.log_prob(action_idx)

        return action_idx.item(), log_prob.item(), value

    # store transitions
    def store(self, transition):
        self.memory.append(transition)

    # -------------------------
    # PPO UPDATE
    # -------------------------
    def update(self, gamma=0.99, eps=0.2):
        states, actions, rewards, log_probs, values = zip(*self.memory)

        returns = []
        G = 0
        for r in reversed(rewards):
            G = r + gamma * G
            returns.insert(0, G)

        returns = torch.tensor(returns, dtype=torch.float32)
        values = torch.tensor(values, dtype=torch.float32)
        actions = torch.tensor(actions)

        advantages = returns - values

        for _ in range(4):  # PPO epochs
            for i in range(len(states)):

                state = states[i]
                action = actions[i]
                old_log = log_probs[i]
                adv = advantages[i]

                state_t = self.preprocess(state)

                logits, value = self.model(state_t)
                probs = F.softmax(logits.squeeze(0), dim=0)

                dist = torch.distributions.Categorical(probs)

                new_log = dist.log_prob(action)

                ratio = torch.exp(new_log - old_log)

                surr1 = ratio * adv
                surr2 = torch.clamp(ratio, 1 - eps, 1 + eps) * adv

                actor_loss = -torch.min(surr1, surr2)

                critic_loss = (returns[i] - value.squeeze()) ** 2

                loss = actor_loss + critic_loss

                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

        self.memory = []