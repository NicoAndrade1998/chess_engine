import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from utils import decode_move, encode_move


# -------------------------
# POLICY NETWORK
# -------------------------
class PolicyNet(nn.Module):
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
            nn.ReLU(),
            nn.Linear(512, 4096)  # 4096 moves
        )

    def forward(self, x):
        x = self.conv(x)
        return self.fc(x)


# -------------------------
# AGENT
# -------------------------
class ChessAgent:
    def __init__(self):
        self.model = PolicyNet()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=1e-4)

    def board_to_tensor(self, board):
        # board is (8,8,12)
        tensor = torch.tensor(board, dtype=torch.float32)
        return tensor.permute(2, 0, 1).unsqueeze(0)  # (1,12,8,8)

    # -------------------------
    # ACTION MASKING
    # -------------------------
    def get_action_mask(self, env):
        mask = np.zeros(4096, dtype=np.float32)

        legal_moves = env.get_legal_moves()

        for move in legal_moves:
            idx = encode_move(move)
            mask[idx] = 1.0

        return mask

    # -------------------------
    # SELECT ACTION
    # -------------------------
    def select_action(self, state, env):
        state = self.board_to_tensor(state)

        logits = self.model(state).detach().squeeze(0).numpy()

        mask = self.get_action_mask(env)

        # VERY IMPORTANT: remove illegal moves
        masked_logits = logits + (mask - 1) * 1e9  # huge negative for illegal

        probs = F.softmax(torch.tensor(masked_logits), dim=0).numpy()

        action_idx = np.random.choice(4096, p=probs)

        return decode_move(action_idx)