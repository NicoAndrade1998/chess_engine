import numpy as np

class ChessEnv:
    def __init__(self):
        piece_values = {
            "pawn": 1,
            "knight": 3,
            "bishop": 3,
            "rook": 5,
            "queen": 9,
            "king": 0
        }

        self.start_board = np.array([
            ["B_rook","B_knight","B_bishop","B_queen","B_king","B_bishop","B_knight","B_rook"],
            ["B_pawn","B_pawn","B_pawn","B_pawn","B_pawn","B_pawn","B_pawn","B_pawn"],
            [".",".",".",".",".",".",".","."],
            [".",".",".",".",".",".",".","."],
            [".",".",".",".",".",".",".","."],
            [".",".",".",".",".",".",".","."],
            ["W_pawn","W_pawn","W_pawn","W_pawn","W_pawn","W_pawn","W_pawn","W_pawn"],
            ["W_rook","W_knight","W_bishop","W_queen","W_king","W_bishop","W_knight","W_rook"]
        ])
        self.reset()


        # -------------------------
            # BOARD ENCODING
            # -------------------------

    # -------------------------
    # RESET
    # -------------------------
    def reset(self):
        self.board = self.start_board.copy()
        self.done = False
        self.turn = "W"
        return self.encode_board()

    # -------------------------
    # APPLY MOVE
    # -------------------------
    def apply_move(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2

        piece = self.board[x1][y1]
        self.board[x2][y2] = piece
        self.board[x1][y1] = "."

    # -------------------------
    # MOVE VALIDATION (fixed + safe)
    # -------------------------
    def moveIsLegal(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2

        # bounds safety (optional but good)
        if not (0 <= x2 < 8 and 0 <= y2 < 8):
            return False

        piece = self.board[x1][y1]
        target = self.board[x2][y2]

        if piece == ".":
            return False

        # cannot capture own piece
        if target != "." and target[0] == piece[0]:
            return False

        dx = x2 - x1
        dy = y2 - y1
        color = piece[0]

        # ---------------- PAWN ----------------
        if piece.endswith("pawn"):
            direction = -1 if color == "W" else 1
            start_row = 6 if color == "W" else 1

            # forward
            if dy == 0 and target == ".":
                if dx == direction:
                    return True
                if x1 == start_row and dx == 2 * direction:
                    mid = x1 + direction
                    if self.board[mid][y1] == ".":
                        return True

            # capture
            if abs(dy) == 1 and dx == direction:
                if target != "." and target[0] != color:
                    return True

            return False

        # ---------------- ROOK ----------------
        if piece.endswith("rook"):
            return self._rook_like(p1, p2)

        # ---------------- KNIGHT ----------------
        if piece.endswith("knight"):
            return (abs(dx), abs(dy)) in [(2, 1), (1, 2)]

        # ---------------- BISHOP ----------------
        if piece.endswith("bishop"):
            return self._bishop_like(p1, p2)

        # ---------------- QUEEN ----------------
        if piece.endswith("queen"):
            return self._rook_like(p1, p2) or self._bishop_like(p1, p2)

        # ---------------- KING ----------------
        if piece.endswith("king"):
            return abs(dx) <= 1 and abs(dy) <= 1

        return False

    # helpers for queen
    def _rook_like(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        if x1 == x2 or y1 == y2:
            return self._path_clear(p1, p2)
        return False

    def _bishop_like(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        if abs(x2 - x1) == abs(y2 - y1):
            return self._path_clear(p1, p2)
        return False

    def _path_clear(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2

        dx = 0 if x2 == x1 else (1 if x2 > x1 else -1)
        dy = 0 if y2 == y1 else (1 if y2 > y1 else -1)

        x, y = x1 + dx, y1 + dy
        while (x, y) != (x2, y2):
            if self.board[x][y] != ".":
                return False
            x += dx
            y += dy

        return True

    # -------------------------
    # STEP (RL INTERFACE)
    # -------------------------
    def step(self, action):
        if self.done:
            return self.board.copy(), 0, True

        (x1, y1), (x2, y2) = action
        piece = self.board[x1][y1]

        if not piece.startswith(self.turn):
            return self.board.copy(), -0.5, False

        if not self.moveIsLegal((x1, y1), (x2, y2)):
            return self.board.copy(), -0.5, False

        reward = 0
        target = self.board[x2][y2]

        if target != ".":
            reward += 0.1

        self.apply_move((x1, y1), (x2, y2))

        # check win BEFORE switching turn
        if not self._king_exists("W") or not self._king_exists("B"):
            self.done = True
            winner = "W" if self._king_exists("W") else "B"
            reward += 1 if winner == self.turn else -1

        # switch turn
        self.turn = "B" if self.turn == "W" else "W"

        return self.encode_board(), reward, self.done
    # -------------------------
    # KING CHECK
    # -------------------------
    def _king_exists(self, color):
        king = f"{color}_king"

        for i in range(8):
            for j in range(8):
                if self.board[i][j] == king:
                    return True
        return False

    # -------------------------
    # LEGAL MOVES (for RL agent)
    # -------------------------
    def get_legal_moves(self):
        moves = []

        for x1 in range(8):
            for y1 in range(8):
                if self.board[x1][y1].startswith(self.turn):
                    for x2 in range(8):
                        for y2 in range(8):
                            if self.moveIsLegal((x1,y1),(x2,y2)):
                                moves.append(((x1,y1),(x2,y2)))

        return moves

    def encode_board(self):
            """
            Returns: 8x8x12 numpy array
            """

            encoding = np.zeros((8, 8, 12), dtype=np.float32)

            piece_to_index = {
                "pawn": 0,
                "rook": 1,
                "knight": 2,
                "bishop": 3,
                "queen": 4,
                "king": 5
            }

            for i in range(8):
                for j in range(8):
                    piece = self.board[i][j]

                    if piece == ".":
                        continue

                    color = piece[0]  # W or B
                    name = piece.split("_")[1]  # pawn, rook, etc.

                    base_idx = piece_to_index[name]

                    # white = 0-5, black = 6-11
                    if color == "W":
                        idx = base_idx
                    else:
                        idx = base_idx + 6

                    encoding[i, j, idx] = 1

            return encoding