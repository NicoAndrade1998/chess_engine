import threading
import numpy as np
import tkinter as tk
from tkinter import *
from tkinter import messagebox

board = np.array([
    ["B_rook","B_knight","B_bishop","B_queen","B_king","B_bishop","B_knight","B_rook"],
    ["B_pawn","B_pawn","B_pawn","B_pawn","B_pawn","B_pawn","B_pawn","B_pawn"],
    [".",".",".",".",".",".",".","."],
    [".",".",".",".",".",".",".","."],
    [".",".",".",".",".",".",".","."],
    [".",".",".",".",".",".",".","."],
    ["W_pawn","W_pawn","W_pawn","W_pawn","W_pawn","W_pawn","W_pawn","W_pawn"],
    ["W_rook","W_knight","W_bishop","W_queen","W_king","W_bishop","W_knight","W_rook"]
])


root = Tk()
root.title("Chess")

UNICODE_MAP = {
    "W_king": "♔", "W_queen": "♕", "W_rook": "♖",
    "W_bishop": "♗", "W_knight": "♘", "W_pawn": "♙",
    "B_king": "♚", "B_queen": "♛", "B_rook": "♜",
    "B_bishop": "♝", "B_knight": "♞", "B_pawn": "♟"
}

canvas = tk.Canvas(root, width=480, height=480)
canvas.pack(fill=BOTH, expand=True)

selected_pos = None   # (row, col) of the piece being dragged
drag_item = None      # canvas item id of the floating piece image
player_can_move = True
game_over = False
_terminal_move_done = threading.Event()  # signals the terminal loop that a full move cycle (player + CPU) finished

#used for drawing the chess board
def get_square_size():
    size = min(canvas.winfo_width(), canvas.winfo_height())
    return max(size // 8, 1)

#used for drawing the chess board
def pixel_to_square(x, y):
    sq = get_square_size()
    col = min(max(x // sq, 0), 7)
    row = min(max(y // sq, 0), 7)
    return row, col

#draws the chess board. I got most of this from google, so i'm not sure how it works ¯\_(ツ)_/¯
def draw_board_gui(highlight=None):
    sq = get_square_size()
    canvas.delete("all")
    colors = ["#F0D9B5", "#B58863"]

    for i in range(8):
        for j in range(8):
            x1 = j * sq
            y1 = i * sq
            x2 = x1 + sq
            y2 = y1 + sq

            color = colors[(i + j) % 2]
            if highlight == (i, j):
                color = "#F6F669"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

            piece = board[i][j]
            if piece != "." and (i, j) != selected_pos:
                symbol = UNICODE_MAP.get(piece, "")
                canvas.create_text(
                    x1 + sq // 2,
                    y1 + sq // 2,
                    text=symbol,
                    font=("Arial", sq // 2)
                )


#handles mouse press: records which white piece the player clicked and begins the drag animation
def on_press(event):
    global selected_pos, drag_item
    if not player_can_move or game_over:
        return
    row, col = pixel_to_square(event.x, event.y)
    piece = board[row][col]
    if piece == "." or piece[0] != "W":
        return
    selected_pos = (row, col)
    draw_board_gui(highlight=(row, col))
    symbol = UNICODE_MAP[piece]
    drag_item = canvas.create_text(
        event.x, event.y,
        text=symbol,
        font=("Arial", get_square_size() // 2),
        tags="drag"
    )


#follows the mouse cursor while the player is dragging a piece
def on_drag(event):
    if drag_item is not None:
        canvas.coords(drag_item, event.x, event.y)


#handles mouse release: validates the drop target, commits the move if legal, then triggers the CPU's turn
def on_release(event):
    global selected_pos, drag_item, player_can_move
    if selected_pos is None:
        return

    canvas.delete("drag")
    drag_item = None

    row, col = pixel_to_square(event.x, event.y)
    dest = (row, col)
    src = selected_pos
    selected_pos = None

    if dest != src and moveIsLegal(src, dest) and not move_leaves_king_in_check(src, dest, "White"):
        move(src, dest)
        check_promotion()
        player_can_move = False
        draw_board_gui()
        root.update()
        if not check_game_over():
            root.after(200, do_cpu_move)
    else:
        draw_board_gui()

#runs cpu_move() on a background thread so the GUI stays responsive, then schedules _after_cpu_move() on the main thread
def do_cpu_move():
    def run():
        cpu_move()
        root.after(0, _after_cpu_move)
    threading.Thread(target=run, daemon=True).start()


#called on the main thread after the CPU finishes its move: checks promotion/game-over and re-enables player input
def _after_cpu_move():
    global player_can_move
    check_promotion()
    draw_board_gui()
    if not check_game_over():
        player_can_move = True
    _terminal_move_done.set()

#moves the desired pieces from point1 to point 2, if such move is legal
def move(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    piece = board[x1][y1]
    opponent = board[x2][y2]
    match piece:
        case "B_pawn":
            if x2 == x1 + 1 and y2 == y1 and board[x2][y2] == ".":
                board[x2][y2] = piece; board[x1][y1] = "."; return True
            elif x2 == x1 + 2 and y2 == y1 and board[x2][y2] == "." and board[x1 + 1][y1] == "." and x1 == 1:
                board[x2][y2] = piece; board[x1][y1] = "."; return True
            elif x2 == x1 + 1 and (y2 == y1 + 1 or y2 == y1 - 1) and board[x2][y2] != "." and board[x2][y2][0] == "W":
                board[x2][y2] = piece; board[x1][y1] = "."; return True
        case "W_pawn":
            if x2 == x1 - 1 and y2 == y1 and board[x2][y2] == ".":
                board[x2][y2] = piece; board[x1][y1] = "."; return True
            elif x2 == x1 - 2 and y2 == y1 and board[x2][y2] == "." and board[x1 - 1][y1] == "." and x1 == 6:
                board[x2][y2] = piece; board[x1][y1] = "."; return True
            elif x2 == x1 - 1 and (y2 == y1 + 1 or y2 == y1 - 1) and board[x2][y2] != "." and board[x2][y2][0] == "B":
                board[x2][y2] = piece; board[x1][y1] = "."; return True
        case "B_rook":
            if opponent[0] == "B": return False
            if x2 == x1 and y2 != y1 and all(board[x1][i] == "." for i in range(min(y1, y2) + 1, max(y1, y2))):
                board[x2][y2] = piece; board[x1][y1] = "."; return True
            elif y2 == y1 and x2 != x1 and all(board[i][y1] == "." for i in range(min(x1, x2) + 1, max(x1, x2))):
                board[x2][y2] = piece; board[x1][y1] = "."; return True
        case "W_rook":
            if opponent[0] == "W": return False
            if x2 == x1 and y2 != y1 and all(board[x1][i] == "." for i in range(min(y1, y2) + 1, max(y1, y2))):
                board[x2][y2] = piece; board[x1][y1] = "."; return True
            elif y2 == y1 and x2 != x1 and all(board[i][y1] == "." for i in range(min(x1, x2) + 1, max(x1, x2))):
                board[x2][y2] = piece; board[x1][y1] = "."; return True
        case "B_knight":
            if opponent[0] == "B": return False
            if (x2 == x1 + 2 and y2 == y1 + 1) or (x2 == x1 + 2 and y2 == y1 - 1) or (x2 == x1 - 2 and y2 == y1 + 1) or (x2 == x1 - 2 and y2 == y1 - 1) or (x2 == x1 + 1 and y2 == y1 + 2) or (x2 == x1 + 1 and y2 == y1 - 2) or (x2 == x1 - 1 and y2 == y1 + 2) or (x2 == x1 - 1 and y2 == y1 - 2):
                if board[x2][y2] == "." or board[x2][y2][0] == "W":
                    board[x2][y2] = piece; board[x1][y1] = "."; return True
        case "W_knight":
            if opponent[0] == "W": return False
            if (x2 == x1 + 2 and y2 == y1 + 1) or (x2 == x1 + 2 and y2 == y1 - 1) or (x2 == x1 - 2 and y2 == y1 + 1) or (x2 == x1 - 2 and y2 == y1 - 1) or (x2 == x1 + 1 and y2 == y1 + 2) or (x2 == x1 + 1 and y2 == y1 - 2) or (x2 == x1 - 1 and y2 == y1 + 2) or (x2 == x1 - 1 and y2 == y1 - 2):
                if board[x2][y2] == "." or board[x2][y2][0] == "B":
                    board[x2][y2] = piece; board[x1][y1] = "."; return True
        case "B_bishop":
            if opponent[0] == "B": return False
            if abs(x2 - x1) == abs(y2 - y1) and all(board[x1 + i*(1 if x2>x1 else -1)][y1 + i*(1 if y2>y1 else -1)] == "." for i in range(1, abs(x2 - x1))):
                board[x2][y2] = piece; board[x1][y1] = "."; return True
        case "W_bishop":
            if opponent[0] == "W": return False
            if abs(x2 - x1) == abs(y2 - y1) and all(board[x1 + i*(1 if x2>x1 else -1)][y1 + i*(1 if y2>y1 else -1)] == "." for i in range(1, abs(x2 - x1))):
                board[x2][y2] = piece; board[x1][y1] = "."; return True
        case "B_queen":
            if opponent[0] == "B": return False
            if (x2 == x1 and y2 != y1 and all(board[x1][i] == "." for i in range(min(y1, y2) + 1, max(y1, y2))) or (y2 == y1 and x2 != x1 and all(board[i][y1] == "." for i in range(min(x1, x2) + 1, max(x1, x2))) or (abs(x2 - x1) == abs(y2 - y1) and all(board[x1 + i*(1 if x2>x1 else -1)][y1 + i*(1 if y2>y1 else -1)] == "." for i in range(1, abs(x2 - x1)))))):
                board[x2][y2] = piece; board[x1][y1] = "."; return True
        case "W_queen":
            if opponent[0] == "W": return False
            if (x2 == x1 and y2 != y1 and all(board[x1][i] == "." for i in range(min(y1, y2) + 1, max(y1, y2))) or (y2 == y1 and x2 != x1 and all(board[i][y1] == "." for i in range(min(x1, x2) + 1, max(x1, x2))) or (abs(x2 - x1) == abs(y2 - y1) and all(board[x1 + i*(1 if x2>x1 else -1)][y1 + i*(1 if y2>y1 else -1)] == "." for i in range(1, abs(x2 - x1)))))):
                board[x2][y2] = piece; board[x1][y1] = "."; return True
        case "B_king":
            if opponent[0] == "B": return False
            if abs(x2 - x1) <= 1 and abs(y2 - y1) <= 1 and (board[x2][y2] == "." or board[x2][y2][0] == "W"):
                board[x2][y2] = piece; board[x1][y1] = "."; return True
        case "W_king":
            if opponent[0] == "W": return False
            if abs(x2 - x1) <= 1 and abs(y2 - y1) <= 1 and (board[x2][y2] == "." or board[x2][y2][0] == "B"):
                board[x2][y2] = piece; board[x1][y1] = "."; return True
        case _:
            return False
    return False

#determines if the move from point1 to point2 is legal
def moveIsLegal(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    piece = board[x1][y1]
    opponent = board[x2][y2]
    match piece:
        case "B_pawn":
            if x2 == x1 + 1 and y2 == y1 and board[x2][y2] == ".": return True
            elif x2 == x1 + 2 and y2 == y1 and board[x2][y2] == "." and board[x1 + 1][y1] == "." and x1 == 1: return True
            elif x2 == x1 + 1 and (y2 == y1 + 1 or y2 == y1 - 1) and board[x2][y2] != "." and board[x2][y2][0] == "W": return True
        case "W_pawn":
            if x2 == x1 - 1 and y2 == y1 and board[x2][y2] == ".": return True
            elif x2 == x1 - 2 and y2 == y1 and board[x2][y2] == "." and board[x1 - 1][y1] == "." and x1 == 6: return True
            elif x2 == x1 - 1 and (y2 == y1 + 1 or y2 == y1 - 1) and board[x2][y2] != "." and board[x2][y2][0] == "B": return True
        case "B_rook":
            if opponent[0] == "B": return False
            if x2 == x1 and y2 != y1 and all(board[x1][i] == "." for i in range(min(y1, y2) + 1, max(y1, y2))): return True
            elif y2 == y1 and x2 != x1 and all(board[i][y1] == "." for i in range(min(x1, x2) + 1, max(x1, x2))): return True
        case "W_rook":
            if opponent[0] == "W": return False
            if x2 == x1 and y2 != y1 and all(board[x1][i] == "." for i in range(min(y1, y2) + 1, max(y1, y2))): return True
            elif y2 == y1 and x2 != x1 and all(board[i][y1] == "." for i in range(min(x1, x2) + 1, max(x1, x2))): return True
        case "B_knight":
            if opponent[0] == "B": return False
            if (x2 == x1 + 2 and y2 == y1 + 1) or (x2 == x1 + 2 and y2 == y1 - 1) or (x2 == x1 - 2 and y2 == y1 + 1) or (x2 == x1 - 2 and y2 == y1 - 1) or (x2 == x1 + 1 and y2 == y1 + 2) or (x2 == x1 + 1 and y2 == y1 - 2) or (x2 == x1 - 1 and y2 == y1 + 2) or (x2 == x1 - 1 and y2 == y1 - 2):
                if board[x2][y2] == "." or board[x2][y2][0] == "W": return True
        case "W_knight":
            if opponent[0] == "W": return False
            if (x2 == x1 + 2 and y2 == y1 + 1) or (x2 == x1 + 2 and y2 == y1 - 1) or (x2 == x1 - 2 and y2 == y1 + 1) or (x2 == x1 - 2 and y2 == y1 - 1) or (x2 == x1 + 1 and y2 == y1 + 2) or (x2 == x1 + 1 and y2 == y1 - 2) or (x2 == x1 - 1 and y2 == y1 + 2) or (x2 == x1 - 1 and y2 == y1 - 2):
                if board[x2][y2] == "." or board[x2][y2][0] == "B": return True
        case "B_bishop":
            if opponent[0] == "B": return False
            if abs(x2 - x1) == abs(y2 - y1) and all(board[x1 + i*(1 if x2>x1 else -1)][y1 + i*(1 if y2>y1 else -1)] == "." for i in range(1, abs(x2 - x1))): return True
        case "W_bishop":
            if opponent[0] == "W": return False
            if abs(x2 - x1) == abs(y2 - y1) and all(board[x1 + i*(1 if x2>x1 else -1)][y1 + i*(1 if y2>y1 else -1)] == "." for i in range(1, abs(x2 - x1))): return True
        case "B_queen":
            if opponent[0] == "B": return False
            if (x2 == x1 and y2 != y1 and all(board[x1][i] == "." for i in range(min(y1, y2) + 1, max(y1, y2))) or (y2 == y1 and x2 != x1 and all(board[i][y1] == "." for i in range(min(x1, x2) + 1, max(x1, x2))) or (abs(x2 - x1) == abs(y2 - y1) and all(board[x1 + i*(1 if x2>x1 else -1)][y1 + i*(1 if y2>y1 else -1)] == "." for i in range(1, abs(x2 - x1)))))): return True
        case "W_queen":
            if opponent[0] == "W": return False
            if (x2 == x1 and y2 != y1 and all(board[x1][i] == "." for i in range(min(y1, y2) + 1, max(y1, y2))) or (y2 == y1 and x2 != x1 and all(board[i][y1] == "." for i in range(min(x1, x2) + 1, max(x1, x2))) or (abs(x2 - x1) == abs(y2 - y1) and all(board[x1 + i*(1 if x2>x1 else -1)][y1 + i*(1 if y2>y1 else -1)] == "." for i in range(1, abs(x2 - x1)))))): return True
        case "B_king":
            if opponent[0] == "B": return False
            if abs(x2 - x1) <= 1 and abs(y2 - y1) <= 1 and (board[x2][y2] == "." or board[x2][y2][0] == "W"): return True
        case "W_king":
            if opponent[0] == "W": return False
            if abs(x2 - x1) <= 1 and abs(y2 - y1) <= 1 and (board[x2][y2] == "." or board[x2][y2][0] == "B"): return True
        case _:
            return False
    return False

#checks if the specified king is currenly in check by the other player. If any of the other player's pieces can move to the space of the indicated player's king, he is in check.
def is_in_check(color):
    king_pos = None
    match color:
        case "White":
            for i in range(8):
                for j in range(8):
                    if board[i][j] == "W_king":
                        king_pos = (i, j)
                        break
        case "Black":
            for i in range(8):
                for j in range(8):
                    if board[i][j] == "B_king":
                        king_pos = (i, j)
                        break
        case _:
            return False

    opponent_color = "B" if color == "White" else "W"
    for i in range(8):
        for j in range(8):
            if board[i][j].startswith(opponent_color):
                if moveIsLegal((i, j), king_pos):
                    return True
    return False

#Determines if the specified move takes king out of checl
def move_leaves_king_in_check(src, dest, color):
    x1, y1 = src
    x2, y2 = dest
    saved_src = board[x1][y1]
    saved_dest = board[x2][y2]
    board[x2][y2] = board[x1][y1]
    board[x1][y1] = "."
    result = is_in_check(color)
    board[x1][y1] = saved_src
    board[x2][y2] = saved_dest
    return result

#checks all possible moves to determine if the player has *any* legal moves.
def has_legal_moves(color):
    prefix = color[0]
    for x1 in range(8):
        for y1 in range(8):
            if board[x1][y1].startswith(prefix):
                for x2 in range(8):
                    for y2 in range(8):
                        if moveIsLegal((x1, y1), (x2, y2)):
                            if not move_leaves_king_in_check((x1, y1), (x2, y2), color):
                                return True
    return False


#opens a modal dialog letting the player choose which piece to promote a pawn to; returns the chosen piece name
def ask_promotion():
    choice = {"piece": "queen"}
    dialog = tk.Toplevel(root)
    dialog.title("Pawn Promotion")
    dialog.resizable(False, False)
    dialog.grab_set()
    tk.Label(dialog, text="Promote pawn to:").pack(pady=8)
    for name in ["queen", "rook", "bishop", "knight"]:
        def make_cb(n):
            def cb():
                choice["piece"] = n
                dialog.destroy()
            return cb
        tk.Button(dialog, text=name.capitalize(), width=12, command=make_cb(name)).pack(pady=2)
    root.wait_window(dialog)
    return choice["piece"]


#scans the back ranks for pawns that reached the end; white gets a player-chosen piece, black auto-promotes to queen
def check_promotion():
    for j in range(8):
        if board[0][j] == "W_pawn":
            piece = ask_promotion()
            board[0][j] = f"W_{piece}"
    for j in range(8):
        if board[7][j] == "B_pawn":
            board[7][j] = "B_queen"


#checks for king capture, checkmate, and stalemate; shows a result dialog and sets game_over if the game has ended
def check_game_over():
    global game_over
    white_king = any(board[i][j] == "W_king" for i in range(8) for j in range(8))
    black_king = any(board[i][j] == "B_king" for i in range(8) for j in range(8))

    if not black_king:
        game_over = True
        messagebox.showinfo("Game Over", "White wins!")
        return True
    if not white_king:
        game_over = True
        messagebox.showinfo("Game Over", "Black wins!")
        return True

    black_stuck = not has_legal_moves("Black")
    white_stuck = not has_legal_moves("White")

    if is_in_check("Black") and black_stuck:
        game_over = True
        messagebox.showinfo("Game Over", "Checkmate! White wins!")
        return True
    if is_in_check("White") and white_stuck:
        game_over = True
        messagebox.showinfo("Game Over", "Checkmate! Black wins!")
        return True
    if black_stuck or white_stuck:
        game_over = True
        messagebox.showinfo("Game Over", "Stalemate!")
        return True

    return False

#selects a piece at random and moves in a random valid direction. If CPU player is in check, it will move the enemy king in a random direction.
def cpu_move():
    x1, y1 = np.random.randint(0, 8), np.random.randint(0, 8)
    target = board[x1][y1]
    move_count = 0

    while target[0] != "B":
        x1, y1 = np.random.randint(0, 8), np.random.randint(0, 8)
        target = board[x1][y1]

    x2, y2 = np.random.randint(0, 8), np.random.randint(0, 8)
    while not moveIsLegal((x1, y1), (x2, y2)) or move_leaves_king_in_check((x1, y1), (x2, y2), "Black"):
        move_count += 1
        x2, y2 = np.random.randint(0, 8), np.random.randint(0, 8)
        if move_count > 8:
            move_count = 0
            x1, y1 = np.random.randint(0, 8), np.random.randint(0, 8)
            target = board[x1][y1]
            while target[0] != "B":
                x1, y1 = np.random.randint(0, 8), np.random.randint(0, 8)
                target = board[x1][y1]
    if moveIsLegal((x1, y1), (x2, y2)):
        move((x1, y1), (x2, y2))


#used to print current layout of the chess board to the screen
def print_board():
    for i in range(8):
        print(" ".join(f"{num:8}" for num in board[i]) + f" {i}")
    print("0        1        2        3        4        5        6        7\n")


# runs in a background thread; mirrors the original terminal input loop — type '6 0 4 0' to move, 'exit' to quit
def terminal_input_loop():
    print_board()
    while True:
        move_input = input("(e.g. '6 0 4 0' to move the piece at (6,0) to (4,0) or 'exit': ")

        if move_input.lower() == "exit":
            root.quit()
            break

        try:
            x1, y1, x2, y2 = map(int, move_input.split())
            src, dest = (x1, y1), (x2, y2)
            _terminal_move_done.clear()
            root.after(0, lambda s=src, d=dest: _handle_terminal_move(s, d))
            _terminal_move_done.wait()  # block until the full move cycle (player + CPU) completes
            print_board()
        except Exception:
            print("Invalid input.")


# processes a terminal move on the main thread so it integrates with the GUI and CPU turn logic
def _handle_terminal_move(src, dest):
    global player_can_move
    if not player_can_move or game_over:
        print("Not your turn or game is over.")
        _terminal_move_done.set()
        return
    if moveIsLegal(src, dest) and not move_leaves_king_in_check(src, dest, "White"):
        move(src, dest)
        check_promotion()
        player_can_move = False
        draw_board_gui()
        root.update()
        if not check_game_over():
            root.after(200, do_cpu_move)
        else:
            _terminal_move_done.set()  # game ended, no CPU move coming
    else:
        print("Illegal move.")
        _terminal_move_done.set()


#wires up mouse event handlers, sets a minimum window size, draws the initial board, and starts the Tkinter event loop
def main():
    canvas.bind("<ButtonPress-1>", on_press)
    canvas.bind("<B1-Motion>", on_drag)
    canvas.bind("<ButtonRelease-1>", on_release)
    canvas.bind("<Configure>", lambda _: draw_board_gui())
    root.minsize(240, 240)
    draw_board_gui()
    threading.Thread(target=terminal_input_loop, daemon=True).start()
    root.mainloop()


if __name__ == "__main__":
    main()
