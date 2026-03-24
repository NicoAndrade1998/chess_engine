import numpy as np #used for better implementation of multidimensional arrays
import tkinter as tk
from tkinter import *

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
root = Tk()
root.title("Chess")

#This is used for drawing with tkinter
UNICODE_MAP = {
    "W_king": "♔", "W_queen": "♕", "W_rook": "♖",
    "W_bishop": "♗", "W_knight": "♘", "W_pawn": "♙",
    "B_king": "♚", "B_queen": "♛", "B_rook": "♜",
    "B_bishop": "♝", "B_knight": "♞", "B_pawn": "♟"
}

canvas = tk.Canvas(root, width=480, height=480)
canvas.pack()


def draw_board_gui():
    canvas.delete("all")
    square_size = 60
    colors = ["#F0D9B5", "#B58863"]

    for i in range(8):
        for j in range(8):
            x1 = j * square_size
            y1 = i * square_size
            x2 = x1 + square_size
            y2 = y1 + square_size

            color = colors[(i + j) % 2]
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

            piece = board[i][j]
            if piece != ".":
                symbol = UNICODE_MAP.get(piece, "")
                canvas.create_text(
                    x1 + square_size // 2,
                    y1 + square_size // 2,
                    text=symbol,
                    font=("Arial", square_size // 2)
                )

#used to print current layout of the chess board to the screen
def print_board():
    for i in range(8):
        print(" ".join(f"{num:8}" for num in board[i]) + f" {i}")
    print("0        1        2        3        4        5        6        7\n")


#moves the indicated piece, if move is legal
#arguments: point1, point2: tuple of form (x,y)
def move(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    piece = board[x1][y1]

    match piece:
        case "B_pawn":
            if x2 == x1 + 1 and y2 == y1 and board[x2][y2] == ".":
                board[x2][y2], board[x1][y1] = piece, "."
            elif x2 == x1 + 2 and y2 == y1 and board[x2][y2] == "." and board[x1 + 1][y1] == "." and x1 == 1:
                board[x2][y2], board[x1][y1] = piece, "."
            elif x2 == x1 + 1 and abs(y2 - y1) == 1 and board[x2][y2] != "." and board[x2][y2][0] == "W":
                board[x2][y2], board[x1][y1] = piece, "."

        case "W_pawn":
            if x2 == x1 - 1 and y2 == y1 and board[x2][y2] == ".":
                board[x2][y2], board[x1][y1] = piece, "."
            elif x2 == x1 - 2 and y2 == y1 and board[x2][y2] == "." and board[x1 - 1][y1] == "." and x1 == 6:
                board[x2][y2], board[x1][y1] = piece, "."
            elif x2 == x1 - 1 and abs(y2 - y1) == 1 and board[x2][y2] != "." and board[x2][y2][0] == "B":
                board[x2][y2], board[x1][y1] = piece, "."

        case "B_rook" | "W_rook":
            if x2 == x1 and all(board[x1][i] == "." for i in range(min(y1, y2)+1, max(y1, y2))):
                board[x2][y2], board[x1][y1] = piece, "."
            elif y2 == y1 and all(board[i][y1] == "." for i in range(min(x1, x2)+1, max(x1, x2))):
                board[x2][y2], board[x1][y1] = piece, "."

        case "B_knight" | "W_knight":
            if (abs(x2-x1), abs(y2-y1)) in [(2,1),(1,2)]:
                if board[x2][y2] == "." or board[x2][y2][0] != piece[0]:
                    board[x2][y2], board[x1][y1] = piece, "."

        case "B_bishop" | "W_bishop":
            if abs(x2-x1) == abs(y2-y1):
                if all(board[x1+i*(1 if x2>x1 else -1)][y1+i*(1 if y2>y1 else -1)] == "." for i in range(1, abs(x2-x1))):
                    board[x2][y2], board[x1][y1] = piece, "."

        case "B_queen" | "W_queen":
            if (x1 == x2 or y1 == y2 or abs(x2-x1) == abs(y2-y1)):
                board[x2][y2], board[x1][y1] = piece, "."

        case "B_king" | "W_king":
            if abs(x2-x1) <= 1 and abs(y2-y1) <= 1:
                board[x2][y2], board[x1][y1] = piece, "."

    #update the GUI after the move
    draw_board_gui()
    root.update()

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
                if move((i, j), king_pos):
                    return True
    return False

def cpu_move():
    x1, y1 = np.random.randint(0, 8), np.random.randint(0, 8)
    while board[x1][y1].charAt(0) != "B": #This assuumes the CPU is playing as black.
        x1, y1 = np.random.randint(0, 8), np.random.randint(0, 8)
    
    

def main():
    draw_board_gui()
    root.update()

    while True:
        root.update()  

        print_board()
        move_input = input("(e.g. '6 0 4 0' to move the piece at (6,0) to (4,0) or 'exit': ")

        if move_input.lower() == "exit":
            break

        try:
            x1, y1, x2, y2 = map(int, move_input.split())
            move((x1, y1), (x2, y2))
        except:
            print("Invalid input.")



if __name__ == "__main__":
    main()
