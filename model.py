import torch
import torch.nn as nn


class PPOModel(nn.Module):
    def __init__(self):
        super().__init__()

        self.shared = nn.Sequential(
            nn.Flatten(),
            nn.Linear(8 * 8 * 12, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU()
        )

        # Policy head probabilities
        self.policy_head = nn.Linear(512, 4096)

        # Value head
        self.value_head = nn.Linear(512, 1)

    def forward(self, x):
        x = self.shared(x)

        logits = self.policy_head(x)   # shape: [batch, 4096]
        value = self.value_head(x)     # shape: [batch, 1]

        return logits, value