import numpy as np #used for better implementation of multidimensional arrays

#B stands for Black, W for White. This array is 8*8 in size and represents all 8 columns and rows of a standard chess board
board = np.array([
         ["B_rook","B_knight","B_bishop","B_queen","B_king","B_bishop","B_knight","B_rook"], 
         ["B_pawn", "B_pawn", "B_pawn", "B_pawn", "B_pawn", "B_pawn", "B_pawn", "B_pawn"],
         [".", ".", ".", ".", ".", ".", ".", "."],
         [".", ".", ".", ".", ".", ".", ".", "."],
         [".", ".", ".", ".", ".", ".", ".", "."],
         [".", ".", ".", ".", ".", ".", ".", "."],
         ["W_pawn", "W_pawn", "W_pawn", "W_pawn", "W_pawn", "W_pawn", "W_pawn", "W_pawn"],
         ["W_rook","W_knight","W_bishop","W_king","W_queen","W_bishop","W_knight","W_rook"]])

#used to print current layout of the chess board to the screen
def print_board():
    for i in range (8):
        print(" ".join(f"{num:8}" for num in board[i]) + f" {i}")
    print("0        1        2        3        4        5        6        7 \n\n")




#moves the indicated piece, if move is legal
#arguments: point1, point2: tuple of form (x,y)
def move(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    piece = board[x1][y1]
    match piece:
        case "B_pawn": #case for Black pawn. Pawn can move 2 spaces on its first move, and 1 space on all subsequent moves. It can also capture pieces diagonally, but cannot move diagonally if there is no piece to capture
            if x2 == x1 + 1 and y2 == y1 and board[x2][y2] == ".":
                board[x2][y2] = piece
                board[x1][y1] = "."
            elif x2 == x1 + 2 and y2 == y1 and board[x2][y2] == "." and board[x1 + 1][y1] == "." and x1 == 1:
                board[x2][y2] = piece
                board[x1][y1] = "."
            elif x2 == x1 + 1 and (y2 == y1 + 1 or y2 == y1 - 1) and board[x2][y2] != "." and board[x2][y2][0] == "W":
                board[x2][y2] = piece
                board[x1][y1] = "."
        case "W_pawn": #case for white pawn. Same as black pawn, but moves in the opposite direction
            if x2 == x1 - 1 and y2 == y1 and board[x2][y2] == ".":
                board[x2][y2] = piece
                board[x1][y1] = "."
            elif x2 == x1 - 2 and y2 == y1 and board[x2][y2] == "." and board[x1 - 1][y1] == "." and x1 == 6:
                board[x2][y2] = piece
                board[x1][y1] = "."
            elif x2 == x1 - 1 and (y2 == y1 + 1 or y2 == y1 - 1) and board[x2][y2] != "." and board[x2][y2][0] == "B":
                board[x2][y2] = piece
                board[x1][y1] = "."
        case "B_rook": #case for black rook. Rook can move any number of spaces in a straight line, but cannot jump over pieces
            if x2 == x1 and y2 != y1 and all(board[x1][i] == "." for i in range(min(y1, y2) + 1, max(y1, y2))):
                board[x2][y2] = piece
                board[x1][y1] = "."
            elif y2 == y1 and x2 != x1 and all(board[i][y1] == "." for i in range(min(x1, x2) + 1, max(x1, x2))):
                board[x2][y2] = piece
                board[x1][y1] = "."
        case "W_rook": #case for white rook. Same as black rook.
            if x2 == x1 and y2 != y1 and all(board[x1][i] == "." for i in range(min(y1, y2) + 1, max(y1, y2))):
                board[x2][y2] = piece
                board[x1][y1] = "."
            elif y2 == y1 and x2 != x1 and all(board[i][y1] == "." for i in range(min(x1, x2) + 1, max(x1, x2))):
                board[x2][y2] = piece
                board[x1][y1] = "."
        case "B_knight": #case for black knight. Knight can move in an L shape, and can jump over pieces
            if (x2 == x1 + 2 and y2 == y1 + 1) or (x2 == x1 + 2 and y2 == y1 - 1) or (x2 == x1 - 2 and y2 == y1 + 1) or (x2 == x1 - 2 and y2 == y1 - 1) or (x2 == x1 + 1 and y2 == y1 + 2) or (x2 == x1 + 1 and y2 == y1 - 2) or (x2 == x1 - 1 and y2 == y1 + 2) or (x2 == x1 - 1 and y2 == y1 - 2):
                if board[x2][y2] == "." or board[x2][y2][0] == "W":
                    board[x2][y2] = piece
                    board[x1][y1] = "."
        case "W_knight": #case for white knight. Same as black knight.
            if (x2 == x1 + 2 and y2 == y1 + 1) or (x2 == x1 + 2 and y2 == y1 - 1) or (x2 == x1 - 2 and y2 == y1 + 1) or (x2 == x1 - 2 and y2 == y1 - 1) or (x2 == x1 + 1 and y2 == y1 + 2) or (x2 == x1 + 1 and y2 == y1 - 2) or (x2 == x1 - 1 and y2 == y1 + 2) or (x2 == x1 - 1 and y2 == y1 - 2):
                if board[x2][y2] == "." or board[x2][y2][0] == "B":
                    board[x2][y2] = piece
                    board[x1][y1] = "."
        case "B_bishop": #case for black bishop. Bishop can move any number of spaces diagonally, but cannot jump over pieces
            if abs(x2 - x1) == abs(y2 - y1) and all(board[x1 + i][y1 + i] == "." for i in range(1, abs(x2 - x1))):
                board[x2][y2] = piece
                board[x1][y1] = "."
        case "W_bishop": #case for white bishop. Same as black bishop.
            if abs(x2 - x1) == abs(y2 - y1) and all(board[x1 + i][y1 + i] == "." for i in range(1, abs(x2 - x1))):
                board[x2][y2] = piece
                board[x1][y1] = "."
        case "B_queen": #case for black queen. Queen can move any number of spaces in a straight line or diagonally, but cannot jump over pieces
            if (x2 == x1 and y2 != y1 and all(board[x1][i] == "." for i in range(min(y1, y2) + 1, max(y1, y2))) or (y2 == y1 and x2 != x1 and all(board[i][y1] == "." for i in range(min(x1, x2) + 1, max(x1, x2))) or (abs(x2 - x1) == abs(y2 - y1) and all(board[x1 + i][y1 + i] == "." for i in range(1, abs(x2 - x1)))))):
                board[x2][y2] = piece
                board[x1][y1] = "."
        case "W_queen": #case for white queen. Same as black queen.
            if (x2 == x1 and y2 != y1 and all(board[x1][i] == "." for i in range(min(y1, y2) + 1, max(y1, y2))) or (y2 == y1 and x2 != x1 and all(board[i][y1] == "." for i in range(min(x1, x2) + 1, max(x1, x2))) or (abs(x2 - x1) == abs(y2 - y1) and all(board[x1 + i][y1 + i] == "." for i in range(1, abs(x2 - x1)))))):
                board[x2][y2] = piece
                board[x1][y1] = "."
        case "B_king": #case for black king. King can move one space in any direction, but cannot move into check
            if abs(x2 - x1) <= 1 and abs(y2 - y1) <= 1 and (board[x2][y2] == "." or board[x2][y2][0] == "W"):
                board[x2][y2] = piece
                board[x1][y1] = "." 
        case "W_king": #case for white king. Same as black king.
            if abs(x2 - x1) <= 1 and abs(y2 - y1) <= 1 and (board[x2][y2] == "." or board[x2][y2][0] == "B"):
                board[x2][y2] = piece
                board[x1][y1] = "."

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

#test function, not implemented
def getPiece(point):
    x, y = point
    print(board[x][y])
    


#The main function loops ad infinitum, printing the board and askint the user for their move.
def main(): 
    while True:
        print_board()
        move_input = input("Enter your move (e.g. '6 0 4 0' to move the piece at (6,0) to (4,0)): ")
        try:
            x1, y1, x2, y2 = map(int, move_input.split())
            move((x1, y1), (x2, y2))
        except ValueError:
            print("Invalid input. Please enter your move in the format 'x1 y1 x2 y2'.")


if __name__ == "__main__":
    main()