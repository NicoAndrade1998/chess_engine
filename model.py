import torch
import torch.nn as nn


class DQN(nn.Module):
    def __init__(self):
        super().__init__()

        self.net = nn.Sequential(
            nn.Flatten(),              # 8x8x12 → 768
            nn.Linear(8 * 8 * 12, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 4096)       # one Q-value per move
        )

    def forward(self, x):
        return self.net(x)