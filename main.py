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
            if abs(x2 - x1) == abs(y2 - y1) and all(board[x1 + i][y1 + i] == "." for i in range(1, abs(x2 - x1))):
                board[x2][y2] = piece
                board[x1][y1] = "."
                return True
        case "W_bishop": #case for white bishop. Same as black bishop.
            if opponent[0] == "W":
                print("Cannot capture your own piece. Try again.")
                return False
            if abs(x2 - x1) == abs(y2 - y1) and all(board[x1 + i][y1 + i] == "." for i in range(1, abs(x2 - x1))):
                board[x2][y2] = piece
                board[x1][y1] = "."
                return True
        
        
        case "B_queen": #case for black queen. Queen can move any number of spaces in a straight line or diagonally, but cannot jump over pieces
            if opponent[0] == "B":
                print("Cannot capture your own piece. Try again.")
                return False
            if (x2 == x1 and y2 != y1 and all(board[x1][i] == "." for i in range(min(y1, y2) + 1, max(y1, y2))) or (y2 == y1 and x2 != x1 and all(board[i][y1] == "." for i in range(min(x1, x2) + 1, max(x1, x2))) or (abs(x2 - x1) == abs(y2 - y1) and all(board[x1 + i][y1 + i] == "." for i in range(1, abs(x2 - x1)))))):
                board[x2][y2] = piece
                board[x1][y1] = "."
                return True
        case "W_queen": #case for white queen. Same as black queen.
            if opponent[0] == "W":
                print("Cannot capture your own piece. Try again.")
                return False
            if (x2 == x1 and y2 != y1 and all(board[x1][i] == "." for i in range(min(y1, y2) + 1, max(y1, y2))) or (y2 == y1 and x2 != x1 and all(board[i][y1] == "." for i in range(min(x1, x2) + 1, max(x1, x2))) or (abs(x2 - x1) == abs(y2 - y1) and all(board[x1 + i][y1 + i] == "." for i in range(1, abs(x2 - x1)))))):
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
                if move((i, j), king_pos):
                    return True
    return False

#basic CPU move funtion. Randomly selects a piece and makes a legal move.
def cpu_move():
    x1, y1 = np.random.randint(0, 8), np.random.randint(0, 8)
    target = board[x1][y1]
    move_count = 0

    while target[0] != "B": #This assumes the CPU is playing as black, and selects a random black piece to move
        x1, y1 = np.random.randint(0, 8), np.random.randint(0, 8)
        target = board[x1][y1]
    
    x2, y2 = np.random.randint(0, 8), np.random.randint(0, 8) #selects a random move for the chosen piece and iterates until it finds a legal move
    while move((x1, y1), (x2, y2)) == False: #certain pieces may not have any legal moves, if that it the case, it loops forever
        move_count = move_count + 1
        #print(move_count) #used for debugging
        x2, y2 = np.random.randint(0, 8), np.random.randint(0, 8)
        
        if move_count > 8: #this is for if the cpu gets stuck in a loop
            move_count = 0 #set counter back to zero
            x1, y1 = np.random.randint(0, 8), np.random.randint(0, 8) #select a new piece at random
            target = board[x1][y1]
            while target[0] != "B": 
                x1, y1 = np.random.randint(0, 8), np.random.randint(0, 8)
                target = board[x1][y1]


    
       

def main():
    draw_board_gui()
    root.update()

    while True:
        draw_board_gui()
        root.update()  

        print_board()
        move_input = input("(e.g. '6 0 4 0' to move the piece at (6,0) to (4,0) or 'exit': ")

        if move_input.lower() == "exit":
            break

        try:
            x1, y1, x2, y2 = map(int, move_input.split())
            #print(move((x1, y1), (x2, y2)))
            if not move((x1,y1),(x2,y2)):
                continue
        except ValueError:
            print("Invalid input.")
        
        cpu_move()



if __name__ == "__main__":
    main()