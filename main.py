import numpy as np
board = np.array([["B_rook","B_knight","B_bishop","B_queen","B_king","B_bishop","B_knight","B_rook"], 
         ["B_pawn", "B_pawn", "B_pawn", "B_pawn", "B_pawn", "B_pawn", "B_pawn", "B_pawn"],
         ["open", "open", "open", "open", "open", "open", "open", "open"],
         ["open", "open", "open", "open", "open", "open", "open", "open"],
         ["open", "open", "open", "open", "open", "open", "open", "open"],
         ["open", "open", "open", "open", "open", "open", "open", "open"],
         ["W_pawn", "W_pawn", "W_pawn", "W_pawn", "W_pawn", "W_pawn", "W_pawn", "W_pawn"],
         ["W_rook","W_knight","W_bishop","W_king","W_queen","W_bishop","W_knight","W_rook"]])

for row in board:
    print(" ".join(f"{num:8}" for num in row))