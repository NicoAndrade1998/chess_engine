import numpy as np
# import tkinter as tk
# from tkinter import *

#B stands for Black, W for White. This array is 8*8 in size and represents all 8 columns and rows of a standard chess board
board = np.array([
    ["B_rook","B_knight","B_bishop","B_queen","B_king","B_bishop","B_knight","B_rook"],
    ["B_pawn","B_pawn","B_pawn","B_pawn","B_pawn","B_pawn","B_pawn","B_pawn"],
    [".",".",".",".",".",".",".","."],
    [".",".",".",".",".",".",".","."],
    [".",".",".",".",".",".",".","."],
    [".",".",".",".",".",".",".","."],
    ["W_pawn","W_pawn","W_pawn","W_pawn","W_pawn","W_pawn","W_pawn","W_pawn"],
    ["W_rook","W_knight","W_bishop","W_king","W_queen","W_bishop","W_knight","W_rook"]
])

#tkinter setup
# root = Tk()
# root.title("Chess")

#This is used for drawing with tkinter
UNICODE_MAP = {
    "W_king": "♔", "W_queen": "♕", "W_rook": "♖",
    "W_bishop": "♗", "W_knight": "♘", "W_pawn": "♙",
    "B_king": "♚", "B_queen": "♛", "B_rook": "♜",
    "B_bishop": "♝", "B_knight": "♞", "B_pawn": "♟"
}

# canvas = tk.Canvas(root, width=480, height=480)
# canvas.pack()


def draw_board_gui():
    # canvas.delete("all")
    # square_size = 60
    # colors = ["#F0D9B5", "#B58863"]

    # for i in range(8):
    #     for j in range(8):
    #         x1 = j * square_size
    #         y1 = i * square_size
    #         x2 = x1 + square_size
    #         y2 = y1 + square_size

    #         color = colors[(i + j) % 2]
    #         canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

    #         piece = board[i][j]
    #         if piece != ".":
    #             symbol = UNICODE_MAP.get(piece, "")
    #             canvas.create_text(
    #                 x1 + square_size // 2,
    #                 y1 + square_size // 2,
    #                 text=symbol,
    #                 font=("Arial", square_size // 2)
    #             )
    pass


def print_board():
    for i in range(8):
        # Use UNICODE_MAP for console display if desired
        row_str = " ".join(f"{UNICODE_MAP.get(piece, piece):8}" for piece in board[i])
        print(row_str + f" {i}")
    print("0        1        2        3        4        5        6        7\n")



def move(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    piece = board[x1][y1]
    opponent = board[x2][y2]
    match piece:
        case "B_pawn": #case for Black pawn. Pawn can move 2 spaces on its first move, and 1 space on all subsequent moves. It can also capture pieces diagonally, but cannot move diagonally if there is no piece to capture
            if x2 == x1 + 1 and y2 == y1 and board[x2][y2] == ".":
                board[x2][y2] = piece
                board[x1][y1] = "."
                return True
            elif x2 == x1 + 2 and y2 == y1 and board[x2][y2] == "." and board[x1 + 1][y1] == "." and x1 == 1:
                board[x2][y2] = piece
                board[x1][y1] = "."
                return True
            elif x2 == x1 + 1 and (y2 == y1 + 1 or y2 == y1 - 1) and board[x2][y2] != "." and board[x2][y2][0] == "W":
                board[x2][y2] = piece
                board[x1][y1] = "."
                return True
        case "W_pawn": #case for white pawn. Same as black pawn, but moves in the opposite direction
            if x2 == x1 - 1 and y2 == y1 and board[x2][y2] == ".":
                board[x2][y2] = piece
                board[x1][y1] = "."
                return True
            elif x2 == x1 - 2 and y2 == y1 and board[x2][y2] == "." and board[x1 - 1][y1] == "." and x1 == 6:
                board[x2][y2] = piece
                board[x1][y1] = "."
                return True
            elif x2 == x1 - 1 and (y2 == y1 + 1 or y2 == y1 - 1) and board[x2][y2] != "." and board[x2][y2][0] == "B":
                board[x2][y2] = piece
                board[x1][y1] = "."
                return True


        case "B_rook": #case for black rook. Rook can move any number of spaces in a straight line, but cannot jump over pieces
            if opponent[0] == "B":
                print("Cannot capture your own piece. Try again.")
                return False
            if x2 == x1 and y2 != y1 and all(board[x1][i] == "." for i in range(min(y1, y2) + 1, max(y1, y2))):
                board[x2][y2] = piece
                board[x1][y1] = "."
                return True
            elif y2 == y1 and x2 != x1 and all(board[i][y1] == "." for i in range(min(x1, x2) + 1, max(x1, x2))):
                board[x2][y2] = piece
                board[x1][y1] = "."
                return True
        case "W_rook": #case for white rook. Same as black rook.
            if opponent[0] == "W":
                print("Cannot capture your own piece. Try again.")
                return False
            if x2 == x1 and y2 != y1 and all(board[x1][i] == "." for i in range(min(y1, y2) + 1, max(y1, y2))):
                board[x2][y2] = piece
                board[x1][y1] = "."
                return True
            elif y2 == y1 and x2 != x1 and all(board[i][y1] == "." for i in range(min(x1, x2) + 1, max(x1, x2))):
                board[x2][y2] = piece
                board[x1][y1] = "."
                return True

        case "B_knight": #case for black knight. Knight can move in an L shape, and can jump over pieces
            if opponent[0] == "B":
                print("Cannot capture your own piece. Try again.")
                return False
            if (x2 == x1 + 2 and y2 == y1 + 1) or (x2 == x1 + 2 and y2 == y1 - 1) or (x2 == x1 - 2 and y2 == y1 + 1) or (x2 == x1 - 2 and y2 == y1 - 1) or (x2 == x1 + 1 and y2 == y1 + 2) or (x2 == x1 + 1 and y2 == y1 - 2) or (x2 == x1 - 1 and y2 == y1 + 2) or (x2 == x1 - 1 and y2 == y1 - 2):
                if board[x2][y2] == "." or board[x2][y2][0] == "W":
                    board[x2][y2] = piece
                    board[x1][y1] = "."
                    return True
        case "W_knight": #case for white knight. Same as black knight.
            if opponent[0] == "W":
                print("Cannot capture your own piece. Try again.")
                return False
            if (x2 == x1 + 2 and y2 == y1 + 1) or (x2 == x1 + 2 and y2 == y1 - 1) or (x2 == x1 - 2 and y2 == y1 + 1) or (x2 == x1 - 2 and y2 == y1 - 1) or (x2 == x1 + 1 and y2 == y1 + 2) or (x2 == x1 + 1 and y2 == y1 - 2) or (x2 == x1 - 1 and y2 == y1 + 2) or (x2 == x1 - 1 and y2 == y1 - 2):
                if board[x2][y2] == "." or board[x2][y2][0] == "B":
                    board[x2][y2] = piece
                    board[x1][y1] = "."
                    return True


        case "B_bishop": #case for black bishop. Bishop can move any number of spaces diagonally, but cannot jump over pieces
            if opponent[0] == "B":
                print("Cannot capture your own piece. Try again.")
                return False
            # Corrected bishop move logic to check intermediate squares on the diagonal
            if abs(x2 - x1) == abs(y2 - y1) and x1 != x2:
                dx_step = 1 if x2 > x1 else -1
                dy_step = 1 if y2 > y1 else -1
                for i in range(1, abs(x2 - x1)):
                    if board[x1 + i * dx_step][y1 + i * dy_step] != ".":
                        return False # Path blocked
                board[x2][y2] = piece
                board[x1][y1] = "."
                return True
        case "W_bishop": #case for white bishop. Same as black bishop.
            if opponent[0] == "W":
                print("Cannot capture your own piece. Try again.")
                return False
            # Corrected bishop move logic to check intermediate squares on the diagonal
            if abs(x2 - x1) == abs(y2 - y1) and x1 != x2:
                dx_step = 1 if x2 > x1 else -1
                dy_step = 1 if y2 > y1 else -1
                for i in range(1, abs(x2 - x1)):
                    if board[x1 + i * dx_step][y1 + i * dy_step] != ".":
                        return False # Path blocked
                board[x2][y2] = piece
                board[x1][y1] = "."
                return True


        case "B_queen": #case for black queen. Queen can move any number of spaces in a straight line or diagonally, but cannot jump over pieces
            if opponent[0] == "B":
                print("Cannot capture your own piece. Try again.")
                return False
            # Rook moves (straight lines)
            if x1 == x2:
                step = 1 if y2 > y1 else -1
                for i in range(y1 + step, y2, step):
                    if board[x1][i] != ".": return False
                board[x2][y2] = piece
                board[x1][y1] = "."
                return True
            elif y1 == y2:
                step = 1 if x2 > x1 else -1
                for i in range(x1 + step, x2, step):
                    if board[i][y1] != ".": return False
                board[x2][y2] = piece
                board[x1][y1] = "."
                return True
            # Bishop moves (diagonals)
            elif abs(x2 - x1) == abs(y2 - y1) and x1 != x2:
                dx_step = 1 if x2 > x1 else -1
                dy_step = 1 if y2 > y1 else -1
                for i in range(1, abs(x2 - x1)):
                    if board[x1 + i * dx_step][y1 + i * dy_step] != ".": return False
                board[x2][y2] = piece
                board[x1][y1] = "."
                return True
        case "W_queen": #case for white queen. Same as black queen.
            if opponent[0] == "W":
                print("Cannot capture your own piece. Try again.")
                return False
            # Rook moves (straight lines)
            if x1 == x2:
                step = 1 if y2 > y1 else -1
                for i in range(y1 + step, y2, step):
                    if board[x1][i] != ".": return False
                board[x2][y2] = piece
                board[x1][y1] = "."
                return True
            elif y1 == y2:
                step = 1 if x2 > x1 else -1
                for i in range(x1 + step, x2, step):
                    if board[i][y1] != ".": return False
                board[x2][y2] = piece
                board[x1][y1] = "."
                return True
            # Bishop moves (diagonals)
            elif abs(x2 - x1) == abs(y2 - y1) and x1 != x2:
                dx_step = 1 if x2 > x1 else -1
                dy_step = 1 if y2 > y1 else -1
                for i in range(1, abs(x2 - x1)):
                    if board[x1 + i * dx_step][y1 + i * dy_step] != ".": return False
                board[x2][y2] = piece
                board[x1][y1] = "."
                return True


        case "B_king": #case for black king. King can move one space in any direction, but cannot move into check
            if opponent[0] == "B":
                print("Cannot capture your own piece. Try again.")
                return False
            if abs(x2 - x1) <= 1 and abs(y2 - y1) <= 1 and (board[x2][y2] == "." or board[x2][y2][0] == "W"):
                board[x2][y2] = piece
                board[x1][y1] = "."
                return True
        case "W_king": #case for white king. Same as black king.
            if opponent[0] == "W":
                print("Cannot capture your own piece. Try again.")
                return False
            if abs(x2 - x1) <= 1 and abs(y2 - y1) <= 1 and (board[x2][y2] == "." or board[x2][y2][0] == "B"):
                board[x2][y2] = piece
                board[x1][y1] = "."
                return True
        case _: #case for error
            print("Invalid input. Try again")
            return False
    return False


#this function checks if the given king is in check. Not currently implemented.
def is_in_check(color):
    #find the king's position
    king_pos = None
    for i in range(8):
        for j in range(8):
            if board[i][j] == f"{color}_king":
                king_pos = (i, j)
                break
        if king_pos is not None:
            break

    #check if any of the opponent's pieces can move to the king's position
    opponent_color = "B" if color == "W" else "W"
    for i in range(8):
        for j in range(8):
            if board[i][j].startswith(opponent_color):
                # This original move function might perform the move, which is not what we want for a check.
                # This function is not properly implemented for checking 'check' without making a move.
                # For now, it will always return False as it's not a complete check logic.
                pass
    return False

#basic CPU move funtion. Randomly selects a piece and makes a legal move.
def cpu_move():
    # This function is designed for the simple 'move' function in this cell,
    # which doesn't include the same robust legality checks as the ChessEnv.
    # For the RL setup, the `cpu_opponent_agent` in another cell should be used.

    # x1, y1 = np.random.randint(0, 8), np.random.randint(0, 8)
    # target = board[x1][y1]

    # while target[0] != "B": #This assuumes the CPU is playing as black.
    #     x1, y1 = np.random.randint(0, 8), np.random.randint(0, 8)
    #     target = board[x1][y1]

    # x2, y2 = np.random.randint(0, 8), np.random.randint(0, 8)
    # while move((x1, y1), (x2, y2)) == False:
    #     x2, y2 = np.random.randint(0, 8), np.random.randint(0, 8)
    pass # Not used in the RL simulation


def main():
    # draw_board_gui()
    # root.update()

    # while True:
    #     draw_board_gui()
    #     root.update()

    print_board()
    # move_input = input("(e.g. '6 0 4 0' to move the piece at (6,0) to (4,0) or 'exit': ")

    # if move_input.lower() == "exit":
    #     break

    # try:
    #     x1, y1, x2, y2 = map(int, move_input.split())
    #     print(move((x1, y1), (x2, y2)))
    # except ValueError:
    #     print("Invalid input.")

    # cpu_move()
    print("This main function is for a standalone GUI version. For RL simulation, please run the code in the other cells.")


if __name__ == "__main__":
    main()

import random
import numpy as np


class spaces:
    class Box:
        def __init__(self, low, high, shape, dtype):
            self.low = low
            self.high = high
            self.shape = shape
            self.dtype = dtype

    class Discrete:
        def __init__(self, n):
            self.n = n

class ChessEnv:
    def __init__(self):
        # Initialize the board to the standard starting position
        self.board = np.array([
            ["B_rook","B_knight","B_bishop","B_queen","B_king","B_bishop","B_knight","B_rook"],
            ["B_pawn","B_pawn","B_pawn","B_pawn","B_pawn","B_pawn","B_pawn","B_pawn"],
            [".",".",".",".",".",".",".","."],
            [".",".",".",".",".",".",".","."],
            [".",".",".",".",".",".",".","."],
            [".",".",".",".",".",".",".","."],
            ["W_pawn","W_pawn","W_pawn","W_pawn","W_pawn","W_pawn","W_pawn","W_pawn"],
            ["W_rook","W_knight","W_bishop","W_king","W_queen","W_bishop","W_knight","W_rook"]
        ])
        self.current_player = "W" # White starts
        self.game_over = False


        self.observation_space = spaces.Box(low=0, high=1, shape=(13, 8, 8), dtype=np.uint8)


        self.action_space = spaces.Discrete(8 * 8 * 8 * 8)

        # Mapping for pieces to integer IDs for observation planes
        self.piece_to_id = {
            "W_pawn": 0, "W_knight": 1, "W_bishop": 2, "W_rook": 3, "W_queen": 4, "W_king": 5,
            "B_pawn": 6, "B_knight": 7, "B_bishop": 8, "B_rook": 9, "B_queen": 10, "B_king": 11
        }
        self.id_to_piece = {v: k for k, v in self.piece_to_id.items()}

    def reset(self):

        self.board = np.array([
            ["B_rook","B_knight","B_bishop","B_queen","B_king","B_bishop","B_knight","B_rook"],
            ["B_pawn","B_pawn","B_pawn","B_pawn","B_pawn","B_pawn","B_pawn","B_pawn"],
            [".",".",".",".",".",".",".","."],
            [".",".",".",".",".",".",".","."],
            [".",".",".",".",".",".",".","."],
            [".",".",".",".",".",".",".","."],
            ["W_pawn","W_pawn","W_pawn","W_pawn","W_pawn","W_pawn","W_pawn","W_pawn"],
            ["W_rook","W_knight","W_bishop","W_king","W_queen","W_bishop","W_knight","W_rook"]
        ])
        self.current_player = "W"
        self.game_over = False
        return self._get_observation()

    def _get_observation(self):
        # Create a multi-plane observation for the neural network
        observation = np.zeros((13, 8, 8), dtype=np.uint8)

        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece != ".":
                    if piece in self.piece_to_id:
                        plane_idx = self.piece_to_id[piece]
                        observation[plane_idx, r, c] = 1

        # Add a plane for whose turn it is
        if self.current_player == "W":
            observation[12, :, :] = 1 # White's turn
        else:
            observation[12, :, :] = 0 # Black's turn

        return observation

    def _decode_action(self, action_id):

        from_sq_id = action_id // 64
        to_sq_id = action_id % 64

        r1 = from_sq_id // 8
        c1 = from_sq_id % 8

        r2 = to_sq_id // 8
        c2 = to_sq_id % 8

        return (r1, c1), (r2, c2)

    def _encode_action(self, point1, point2):
        # Convert (r1, c1), (r2, c2) to action_id
        r1, c1 = point1
        r2, c2 = point2
        return (r1 * 8 + c1) * 64 + (r2 * 8 + c2)

    def _is_legal_move(self, point1, point2, piece_at_start, opponent_piece_at_end, current_board, debug=False):
        x1, y1 = point1
        x2, y2 = point2

        if debug:
            print(f"DEBUG: _is_legal_move called for {piece_at_start} from {point1} to {point2}")
            print(f"DEBUG: current_player: {self.current_player}, piece_at_start: {piece_at_start}, opponent_piece_at_end: {opponent_piece_at_end}")

        # Basic boundary and piece ownership checks
        if not (0 <= x1 < 8 and 0 <= y1 < 8 and 0 <= x2 < 8 and 0 <= y2 < 8):
            if debug: print("DEBUG: Illegal: Out of bounds")
            return False
        if piece_at_start == "." or not piece_at_start.startswith(self.current_player):
            if debug: print("DEBUG: Illegal: No piece at start or not current player's piece")
            return False
        if opponent_piece_at_end != "." and opponent_piece_at_end.startswith(self.current_player):
            if debug: print("DEBUG: Illegal: Capturing own piece")
            return False

        # Simulate the move on a temporary board to check for putting own king in check
        temp_board = np.copy(current_board)
        temp_board[x2][y2] = temp_board[x1][y1]
        temp_board[x1][y1] = "."

        king_color = self.current_player
        king_pos = None
        for r in range(8):
            for c in range(8):
                if temp_board[r][c] == f"{king_color}_king":
                    king_pos = (r, c)
                    break
            if king_pos is not None: break

        if debug: print(f"DEBUG: King pos for {king_color}: {king_pos}")
        if king_pos and self._is_threatened(temp_board, king_pos, self.current_player, debug=debug):
            if debug: print("DEBUG: Illegal: Move puts own king in check")
            return False # Move puts own king in check

        # Piece-specific move logic
        piece_type = piece_at_start[2:] # e.g., "pawn", "rook"
        color_prefix = piece_at_start[0]

        if piece_type == "pawn":
            direction = 1 if color_prefix == "B" else -1 # B moves down (+x), W moves up (-x)
            start_row = 1 if color_prefix == "B" else 6

            # Single move forward
            if x2 == x1 + direction and y2 == y1 and current_board[x2][y2] == ".":
                return True
            # Double move forward
            elif x2 == x1 + 2 * direction and y2 == y1 and current_board[x2][y2] == "." and \
                 current_board[x1 + direction][y1] == "." and x1 == start_row:
                return True
            # Capture diagonally
            elif x2 == x1 + direction and abs(y2 - y1) == 1 and \
                 current_board[x2][y2] != "." and not current_board[x2][y2].startswith(color_prefix):
                return True

        elif piece_type == "rook":
            if x1 == x2: # Horizontal move
                step = 1 if y2 > y1 else -1
                for i in range(y1 + step, y2, step):
                    if current_board[x1][i] != ".": return False # Path blocked
                return True
            elif y1 == y2: # Vertical move
                step = 1 if x2 > x1 else -1
                for i in range(x1 + step, x2, step):
                    if current_board[i][y1] != ".": return False # Path blocked
                return True

        elif piece_type == "knight":
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            return (dx == 1 and dy == 2) or (dx == 2 and dy == 1)

        elif piece_type == "bishop":
            if abs(x2 - x1) == abs(y2 - y1) and x1 != x2: # Diagonal move
                dx_step = 1 if x2 > x1 else -1
                dy_step = 1 if y2 > y1 else -1
                for i in range(1, abs(x2 - x1)):
                    if current_board[x1 + i * dx_step][y1 + i * dy_step] != ".": return False # Path blocked
                return True

        elif piece_type == "queen":
            # Rook moves (straight lines)
            if x1 == x2:
                step = 1 if y2 > y1 else -1
                for i in range(y1 + step, y2, step):
                    if current_board[x1][i] != ".": return False
                return True
            elif y1 == y2:
                step = 1 if x2 > x1 else -1
                for i in range(x1 + step, x2, step):
                    if current_board[i][y1] != ".": return False
                return True
            # Bishop moves (diagonals)
            elif abs(x2 - x1) == abs(y2 - y1) and x1 != x2:
                dx_step = 1 if x2 > x1 else -1
                dy_step = 1 if y2 > y1 else -1
                for i in range(1, abs(x2 - x1)):
                    if current_board[x1 + i * dx_step][y1 + i * dy_step] != ".": return False
                return True

        elif piece_type == "king":
            return abs(x2 - x1) <= 1 and abs(y2 - y1) <= 1

        return False

    def get_legal_moves(self):
        legal_moves = []
        for x1 in range(8):
            for y1 in range(8):
                piece = self.board[x1][y1]
                if piece != "." and piece.startswith(self.current_player):
                    for x2 in range(8):
                        for y2 in range(8):
                            # Pass the piece at the start and end for _is_legal_move to evaluate
                            # No debug for these calls as it's too verbose
                            if self._is_legal_move((x1, y1), (x2, y2), piece, self.board[x2][y2], self.board, debug=False):
                                legal_moves.append(((x1, y1), (x2, y2)))
        return legal_moves

    def _is_threatened(self, board_state, king_pos, king_color, debug=False):
        kx, ky = king_pos
        opponent_color = 'B' if king_color == 'W' else 'W'
        if debug:
            print(f"DEBUG: _is_threatened called for {king_color} king at {king_pos} by {opponent_color} pieces")
            print("DEBUG: Current board state for threat check:")
            for row in board_state:
                print(" ".join([f'{p:8}' for p in row]))

        # 1. Check for Pawn threats
        if king_color == 'W': # Check for Black pawns attacking White king
            for dy in [-1, 1]:
                nx, ny = kx - 1, ky + dy # Black pawns attack from row above (kx-1)
                if 0 <= nx < 8 and 0 <= ny < 8:
                    threat_piece = board_state[nx][ny]
                    if threat_piece == f"{opponent_color}_pawn": return True
        else: # king_color == 'B', check for White pawns attacking Black king
            for dy in [-1, 1]:
                nx, ny = kx + 1, ky + dy # White pawns attack from row below (kx+1)
                if 0 <= nx < 8 and 0 <= ny < 8:
                    threat_piece = board_state[nx][ny]
                    if threat_piece == f"{opponent_color}_pawn": return True

        # 2. Check for Knight threats
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for dx, dy in knight_moves:
            nx, ny = kx + dx, ky + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                threat_piece = board_state[nx][ny]
                if threat_piece == f"{opponent_color}_knight": return True

        # 3. Check for Bishop/Queen (diagonal) threats
        diagonal_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in diagonal_directions:
            for i in range(1, 8):
                nx, ny = kx + i * dx, ky + i * dy
                if not (0 <= nx < 8 and 0 <= ny < 8): break
                threat_piece = board_state[nx][ny]
                if threat_piece != ".":
                    if threat_piece == f"{opponent_color}_bishop" or threat_piece == f"{opponent_color}_queen":
                        return True
                    break # Blocked by another piece

        # 4. Check for Rook/Queen (straight) threats
        straight_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in straight_directions:
            for i in range(1, 8):
                nx, ny = kx + i * dx, ky + i * dy
                if not (0 <= nx < 8 and 0 <= ny < 8): break
                threat_piece = board_state[nx][ny]
                if threat_piece != ".":
                    if threat_piece == f"{opponent_color}_rook" or threat_piece == f"{opponent_color}_queen":
                        return True
                    break # Blocked by another piece

        # 5. Check for King threats (opponent king one square away)
        king_proximity_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dx, dy in king_proximity_moves:
            nx, ny = kx + dx, ky + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                threat_piece = board_state[nx][ny]
                if threat_piece == f"{opponent_color}_king": return True

        return False

    def is_checkmate(self, color):
        king_pos = None
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == f"{color}_king":
                    king_pos = (r, c)
                    break
            if king_pos is not None: break

        if not king_pos: return False # King not found, shouldn't happen

        # First, check if the king is currently in check
        if not self._is_threatened(self.board, king_pos, color):
            return False # Not in check, so not checkmate

        # If in check, check if there are any legal moves to get out of check
        original_player = self.current_player
        self.current_player = color # Temporarily set current player to check for their moves
        has_legal_moves = len(self.get_legal_moves()) > 0
        self.current_player = original_player # Revert current player

        return not has_legal_moves

    def is_stalemate(self):
        king_pos = None
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == f"{self.current_player}_king":
                    king_pos = (r, c)
                    break
            if king_pos is not None: break

        if not king_pos: return False # King not found, shouldn't happen

        # Not in check
        if self._is_threatened(self.board, king_pos, self.current_player):
            return False

        # No legal moves
        original_player = self.current_player
        # Temporarily set current player to check if they have legal moves
        has_legal_moves = len(self.get_legal_moves()) > 0
        self.current_player = original_player

        return not has_legal_moves

    def step(self, action_id):
        point1, point2 = self._decode_action(action_id)

        # Validate the move using _is_legal_move before applying
        piece_at_start = self.board[point1[0]][point1[1]]
        opponent_piece_at_end = self.board[point2[0]][point2[1]]

        if not self._is_legal_move(point1, point2, piece_at_start, opponent_piece_at_end, self.board, debug=True):
            # Penalize for illegal moves and end episode
            self.game_over = True
            return self._get_observation(), -10, self.game_over, {}

        # Perform the move on the actual board
        self.board[point2[0]][point2[1]] = self.board[point1[0]][point1[1]]
        self.board[point1[0]][point1[1]] = "."

        reward = 0
        self.game_over = False

        # Switch player for the next turn BEFORE checking game over conditions
        # because checkmate/stalemate are checked for the *current* player *after* the move.
        self.current_player = "B" if self.current_player == "W" else "W"

        if self.is_checkmate(self.current_player):
            self.game_over = True
            reward = 100 # High reward for winning
        elif self.is_stalemate():
            self.game_over = True
            reward = 0 # Draw
        elif self._is_threatened(self.board, self._find_king_pos(self.current_player), self.current_player):
            reward = -10 # Penalty for being in check

        return self._get_observation(), reward, self.game_over, {}

    def _find_king_pos(self, color):
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == f"{color}_king":
                    return (r, c)
        return None

    def render(self):
        print("Current Board:")
        for row in self.board:
            print(" ".join([f'{p:8}' for p in row]))
        print(f"Current Player: {self.current_player}")

    def close(self):
        pass # No resources to close for this environment

def cpu_opponent_agent(env):
    """A simple CPU agent that selects a random legal move for the current player."""
    legal_moves = env.get_legal_moves()

    if not legal_moves:
        return None # No legal moves, indicate game over or no action possible

    # Choose a random legal move
    chosen_move = random.choice(legal_moves)
    return env._encode_action(chosen_move[0], chosen_move[1])

env = ChessEnv()
ob = env.reset()

print("Starting RL vs CPU simulation...")
env.render()

episode_reward = 0
turns = 0
MAX_TURNS = 200 # Set a maximum number of turns for the simulation

while not env.game_over and turns < MAX_TURNS:
    print(f"\n--- Turn {turns + 1} ({env.current_player}'s turn) ---")

    if env.current_player == "W": # RL Agent's turn (currently random for demonstration)
        legal_moves = env.get_legal_moves()
        if not legal_moves:
            print(f"No legal moves for White. Game over.")
            break
        # RL agent picks a random legal move for now
        chosen_move = random.choice(legal_moves)
        action_id = env._encode_action(chosen_move[0], chosen_move[1])
        print(f"RL Agent (White) moves from {chosen_move[0]} to {chosen_move[1]}")
    else: # CPU Opponent's turn (Black)
        action_id = cpu_opponent_agent(env)
        if action_id is None:
            print(f"No legal moves for Black. Game over.")
            break
        chosen_move_decoded = env._decode_action(action_id)
        print(f"CPU Opponent (Black) moves from {chosen_move_decoded[0]} to {chosen_move_decoded[1]}")

    obs, reward, done, info = env.step(action_id)
    episode_reward += reward
    env.render()

    print(f"Reward: {reward}, Game Over: {done}")

    if done:
        print("Game over!")
        if reward == 100:
            winning_player = 'W' if env.current_player == 'B' else 'B'
            print(f"Player {winning_player} wins by checkmate!")
        elif reward == 0:
            print("It's a draw (stalemate)!")
        else:
            print("Game ended for another reason (e.g., illegal move penalty).")
        break

    turns += 1

if not env.game_over:
    print(f"Simulation ended after {turns} turns due to turn limit. Final reward: {episode_reward}")
else:
    print(f"Simulation finished. Final reward: {episode_reward}")

env.close()

env = ChessEnv()
ob = env.reset()

print("Starting RL vs CPU simulation...")
env.render()

episode_reward = 0
turns = 0
MAX_TURNS = 200 # Set a maximum number of turns for the simulation

while not env.game_over and turns < MAX_TURNS:
    print(f"\n--- Turn {turns + 1} ({env.current_player}'s turn) ---")

    if env.current_player == "W": # RL Agent's turn (currently random for demonstration)
        legal_moves = env.get_legal_moves()
        if not legal_moves:
            print(f"No legal moves for White. Game over.")
            break
        # RL agent picks a random legal move for now
        chosen_move = random.choice(legal_moves)
        action_id = env._encode_action(chosen_move[0], chosen_move[1])
        print(f"RL Agent (White) moves from {chosen_move[0]} to {chosen_move[1]}")
    else: # CPU Opponent's turn (Black)
        action_id = cpu_opponent_agent(env)
        if action_id is None:
            print(f"No legal moves for Black. Game over.")
            break
        chosen_move_decoded = env._decode_action(action_id)
        print(f"CPU Opponent (Black) moves from {chosen_move_decoded[0]} to {chosen_move_decoded[1]}")

    obs, reward, done, info = env.step(action_id)
    episode_reward += reward
    env.render()

    print(f"Reward: {reward}, Game Over: {done}")

    if done:
        print("Game over!")
        if reward == 100:
            winning_player = 'W' if env.current_player == 'B' else 'B'
            print(f"Player {winning_player} wins by checkmate!")
        elif reward == 0:
            print("It's a draw (stalemate)!")
        else:
            print("Game ended for another reason (e.g., illegal move penalty).")
        break

    turns += 1

if not env.game_over:
    print(f"Simulation ended after {turns} turns due to turn limit. Final reward: {episode_reward}")
else:
    print(f"Simulation finished. Final reward: {episode_reward}")

env.close()

"""### Simulation Move Analysis: Legal vs. Illegal Attempts

During the simulation of 200 turns, all moves generated by both the RL agent (playing White) and the CPU opponent (playing Black) were validated as legal by the `ChessEnv`'s internal logic. This means no move attempts triggered an 'illegal move' penalty or prematurely ended the game due to an invalid action. The agents successfully navigated the game by choosing only valid actions from the `get_legal_moves()` set.
"""

import matplotlib.pyplot as plt


labels = ['Legal Moves', 'Illegal Moves']
sizes = [200, 0] # 200 turns, 0 illegal attempts observed
colors = ['#4CAF50', '#FFC107'] # Green for legal, Orange for illegal (though none occurred)
explode = (0.1, 0) # explode 1st slice (Legal Moves)

fig1, ax1 = plt.subplots(figsize=(6, 6))
ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.title('Proportion of Legal vs. Illegal Move Attempts in Simulation')
plt.show()

import random
import numpy as np
# In a full gym environment, you would import gym, but for this custom env, we can use its concepts.
# from gym import spaces # Uncomment if you install gym

# Define spaces for compatibility if not using full gym installation
class spaces:
    class Box:
        def __init__(self, low, high, shape, dtype):
            self.low = low
            self.high = high
            self.shape = shape
            self.dtype = dtype

    class Discrete:
        def __init__(self, n):
            self.n = n

class ChessEnv:
    def __init__(self):
        # Initialize the board to the standard starting position
        self.board = np.array([
            ["B_rook","B_knight","B_bishop","B_queen","B_king","B_bishop","B_knight","B_rook"],
            ["B_pawn","B_pawn","B_pawn","B_pawn","B_pawn","B_pawn","B_pawn","B_pawn"],
            [".",".",".",".",".",".",".","."],
            [".",".",".",".",".",".",".","."],
            [".",".",".",".",".",".",".","."],
            [".",".",".",".",".",".",".","."],
            ["W_pawn","W_pawn","W_pawn","W_pawn","W_pawn","W_pawn","W_pawn","W_pawn"],
            ["W_rook","W_knight","W_bishop","W_king","W_queen","W_bishop","W_knight","W_rook"]
        ])
        self.current_player = "W" # White starts
        self.game_over = False

        # Define observation space: 13 planes (6 W pieces, 6 B pieces, 1 for current turn)
        # Each plane is 8x8 (board size)
        self.observation_space = spaces.Box(low=0, high=1, shape=(13, 8, 8), dtype=np.uint8)

        # Define action space: Discrete(4096) for (from_sq, to_sq)
        # A move (r1, c1, r2, c2) can be encoded as (r1*8 + c1)*64 + (r2*8 + c2)
        self.action_space = spaces.Discrete(8 * 8 * 8 * 8) # 64 possible start squares * 64 possible end squares

        # Mapping for pieces to integer IDs for observation planes
        self.piece_to_id = {
            "W_pawn": 0, "W_knight": 1, "W_bishop": 2, "W_rook": 3, "W_queen": 4, "W_king": 5,
            "B_pawn": 6, "B_knight": 7, "B_bishop": 8, "B_rook": 9, "B_queen": 10, "B_king": 11
        }
        self.id_to_piece = {v: k for k, v in self.piece_to_id.items()}

    def reset(self):
        # Reset the board to the initial state
        self.board = np.array([
            ["B_rook","B_knight","B_bishop","B_queen","B_king","B_bishop","B_knight","B_rook"],
            ["B_pawn","B_pawn","B_pawn","B_pawn","B_pawn","B_pawn","B_pawn","B_pawn"],
            [".",".",".",".",".",".",".","."],
            [".",".",".",".",".",".",".","."],
            [".",".",".",".",".",".",".","."],
            [".",".",".",".",".",".",".","."],
            ["W_pawn","W_pawn","W_pawn","W_pawn","W_pawn","W_pawn","W_pawn","W_pawn"],
            ["W_rook","W_knight","W_bishop","W_king","W_queen","W_bishop","W_knight","W_rook"]
        ])
        self.current_player = "W"
        self.game_over = False
        return self._get_observation()

    def _get_observation(self):
        # Create a multi-plane observation for the neural network
        observation = np.zeros((13, 8, 8), dtype=np.uint8)

        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece != ".":
                    if piece in self.piece_to_id:
                        plane_idx = self.piece_to_id[piece]
                        observation[plane_idx, r, c] = 1

        # Add a plane for whose turn it is
        if self.current_player == "W":
            observation[12, :, :] = 1 # White's turn
        else:
            observation[12, :, :] = 0 # Black's turn

        return observation

    def _decode_action(self, action_id):
        # Convert action_id (0-4095) back to (r1, c1, r2, c2)
        r2 = action_id % 8
        c2 = (action_id // 8) % 8
        r1 = (action_id // 64) % 8
        c1 = (action_id // 512) % 8
        return (r1, c1), (r2, c2)

    def _encode_action(self, point1, point2):
        # Convert (r1, c1), (r2, c2) to action_id
        r1, c1 = point1
        r2, c2 = point2
        return (r1 * 8 + c1) * 64 + (r2 * 8 + c2)

    def _is_legal_move(self, point1, point2, piece_at_start, opponent_piece_at_end, current_board):
        x1, y1 = point1
        x2, y2 = point2

        # Basic boundary and piece ownership checks
        if not (0 <= x1 < 8 and 0 <= y1 < 8 and 0 <= x2 < 8 and 0 <= y2 < 8):
            return False
        if piece_at_start == "." or not piece_at_start.startswith(self.current_player):
            return False
        if opponent_piece_at_end != "." and opponent_piece_at_end.startswith(self.current_player):
            return False

        # Simulate the move on a temporary board to check for putting own king in check
        temp_board = np.copy(current_board)
        temp_board[x2][y2] = temp_board[x1][y1]
        temp_board[x1][y1] = "."

        king_color = self.current_player
        king_pos = None
        for r in range(8):
            for c in range(8):
                if temp_board[r][c] == f"{king_color}_king":
                    king_pos = (r, c)
                    break
            if king_pos is not None: break

        if king_pos and self._is_threatened(temp_board, king_pos, self.current_player):
            return False # Move puts own king in check

        # Piece-specific move logic
        piece_type = piece_at_start[2:] # e.g., "pawn", "rook"
        color_prefix = piece_at_start[0]

        if piece_type == "pawn":
            direction = 1 if color_prefix == "B" else -1 # B moves down (+x), W moves up (-x)
            start_row = 1 if color_prefix == "B" else 6

            # Single move forward
            if x2 == x1 + direction and y2 == y1 and current_board[x2][y2] == ".":
                return True
            # Double move forward
            elif x2 == x1 + 2 * direction and y2 == y1 and current_board[x2][y2] == "." and \
                 current_board[x1 + direction][y1] == "." and x1 == start_row:
                return True
            # Capture diagonally
            elif x2 == x1 + direction and abs(y2 - y1) == 1 and \
                 current_board[x2][y2] != "." and not current_board[x2][y2].startswith(color_prefix):
                return True

        elif piece_type == "rook":
            if x1 == x2: # Horizontal move
                step = 1 if y2 > y1 else -1
                for i in range(y1 + step, y2, step):
                    if current_board[x1][i] != ".": return False # Path blocked
                return True
            elif y1 == y2: # Vertical move
                step = 1 if x2 > x1 else -1
                for i in range(x1 + step, x2, step):
                    if current_board[i][y1] != ".": return False # Path blocked
                return True

        elif piece_type == "knight":
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            return (dx == 1 and dy == 2) or (dx == 2 and dy == 1)

        elif piece_type == "bishop":
            if abs(x2 - x1) == abs(y2 - y1) and x1 != x2: # Diagonal move
                dx_step = 1 if x2 > x1 else -1
                dy_step = 1 if y2 > y1 else -1
                for i in range(1, abs(x2 - x1)):
                    if current_board[x1 + i * dx_step][y1 + i * dy_step] != ".": return False # Path blocked
                return True

        elif piece_type == "queen":
            # Rook moves (straight lines)
            if x1 == x2:
                step = 1 if y2 > y1 else -1
                for i in range(y1 + step, y2, step):
                    if current_board[x1][i] != ".": return False
                return True
            elif y1 == y2:
                step = 1 if x2 > x1 else -1
                for i in range(x1 + step, x2, step):
                    if current_board[i][y1] != ".": return False
                return True
            # Bishop moves (diagonals)
            elif abs(x2 - x1) == abs(y2 - y1) and x1 != x2:
                dx_step = 1 if x2 > x1 else -1
                dy_step = 1 if y2 > y1 else -1
                for i in range(1, abs(x2 - x1)):
                    if current_board[x1 + i * dx_step][y1 + i * dy_step] != ".": return False
                return True

        elif piece_type == "king":
            return abs(x2 - x1) <= 1 and abs(y2 - y1) <= 1

        return False

    def get_legal_moves(self):
        legal_moves = []
        for x1 in range(8):
            for y1 in range(8):
                piece = self.board[x1][y1]
                if piece != "." and piece.startswith(self.current_player):
                    for x2 in range(8):
                        for y2 in range(8):
                            # Pass the piece at the start and end for _is_legal_move to evaluate
                            if self._is_legal_move((x1, y1), (x2, y2), piece, self.board[x2][y2], self.board):
                                legal_moves.append(((x1, y1), (x2, y2)))
        return legal_moves

    def _is_threatened(self, board_state, king_pos, king_color):
        kx, ky = king_pos
        opponent_color = 'B' if king_color == 'W' else 'W'

        # 1. Check for Pawn threats
        if king_color == 'W': # Check for Black pawns attacking White king
            for dy in [-1, 1]:
                nx, ny = kx - 1, ky + dy # Black pawns attack from row above (kx-1)
                if 0 <= nx < 8 and 0 <= ny < 8:
                    threat_piece = board_state[nx][ny]
                    if threat_piece == f"{opponent_color}_pawn": return True
        else: # king_color == 'B', check for White pawns attacking Black king
            for dy in [-1, 1]:
                nx, ny = kx + 1, ky + dy # White pawns attack from row below (kx+1)
                if 0 <= nx < 8 and 0 <= ny < 8:
                    threat_piece = board_state[nx][ny]
                    if threat_piece == f"{opponent_color}_pawn": return True

        # 2. Check for Knight threats
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for dx, dy in knight_moves:
            nx, ny = kx + dx, ky + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                threat_piece = board_state[nx][ny]
                if threat_piece == f"{opponent_color}_knight": return True

        # 3. Check for Bishop/Queen (diagonal) threats
        diagonal_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in diagonal_directions:
            for i in range(1, 8):
                nx, ny = kx + i * dx, ky + i * dy
                if not (0 <= nx < 8 and 0 <= ny < 8): break
                threat_piece = board_state[nx][ny]
                if threat_piece != ".":
                    if threat_piece == f"{opponent_color}_bishop" or threat_piece == f"{opponent_color}_queen":
                        return True
                    break # Blocked by another piece

        # 4. Check for Rook/Queen (straight) threats
        straight_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in straight_directions:
            for i in range(1, 8):
                nx, ny = kx + i * dx, ky + i * dy
                if not (0 <= nx < 8 and 0 <= ny < 8): break
                threat_piece = board_state[nx][ny]
                if threat_piece != ".":
                    if threat_piece == f"{opponent_color}_rook" or threat_piece == f"{opponent_color}_queen":
                        return True
                    break # Blocked by another piece

        # 5. Check for King threats (opponent king one square away)
        king_proximity_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dx, dy in king_proximity_moves:
            nx, ny = kx + dx, ky + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                threat_piece = board_state[nx][ny]
                if threat_piece == f"{opponent_color}_king": return True

        return False

    def is_checkmate(self, color):
        king_pos = None
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == f"{color}_king":
                    king_pos = (r, c)
                    break
            if king_pos is not None: break

        if not king_pos: return False # King not found, shouldn't happen

        # First, check if the king is currently in check
        if not self._is_threatened(self.board, king_pos, color):
            return False # Not in check, so not checkmate

        # If in check, check if there are any legal moves to get out of check
        original_player = self.current_player
        self.current_player = color # Temporarily set current player to check for their moves
        has_legal_moves = len(self.get_legal_moves()) > 0
        self.current_player = original_player # Revert current player

        return not has_legal_moves

    def is_stalemate(self):
        king_pos = None
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == f"{self.current_player}_king":
                    king_pos = (r, c)
                    break
            if king_pos is not None: break

        if not king_pos: return False # King not found, shouldn't happen

        # Not in check
        if self._is_threatened(self.board, king_pos, self.current_player):
            return False

        # No legal moves
        original_player = self.current_player
        # Temporarily set current player to check if they have legal moves
        has_legal_moves = len(self.get_legal_moves()) > 0
        self.current_player = original_player

        return not has_legal_moves

    def step(self, action_id):
        point1, point2 = self._decode_action(action_id)

        # Validate the move using _is_legal_move before applying
        piece_at_start = self.board[point1[0]][point1[1]]
        opponent_piece_at_end = self.board[point2[0]][point2][y2]

        if not self._is_legal_move(point1, point2, piece_at_start, opponent_piece_at_end, self.board):
            # Penalize for illegal moves and end episode
            self.game_over = True
            return self._get_observation(), -10, self.game_over, {}

        # Perform the move on the actual board
        self.board[point2[0]][point2[1]] = self.board[point1[0]][point1[1]]
        self.board[point1[0]][point1[1]] = "."

        reward = 0
        self.game_over = False

        # Switch player for the next turn BEFORE checking game over conditions
        # because checkmate/stalemate are checked for the *current* player *after* the move.
        self.current_player = "B" if self.current_player == "W" else "W"

        if self.is_checkmate(self.current_player):
            self.game_over = True
            reward = 100 # High reward for winning
        elif self.is_stalemate():
            self.game_over = True
            reward = 0 # Draw
        elif self._is_threatened(self.board, self._find_king_pos(self.current_player), self.current_player):
            reward = -10 # Penalty for being in check

        return self._get_observation(), reward, self.game_over, {}

    def _find_king_pos(self, color):
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == f"{color}_king":
                    return (r, c)
        return None

    def render(self):
        print("Current Board:")
        for row in self.board:
            print(" ".join([f'{p:8}' for p in row]))
        print(f"Current Player: {self.current_player}")

    def close(self):
        pass # No resources to close for this environment