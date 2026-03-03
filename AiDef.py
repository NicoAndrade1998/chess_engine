##Implementation follows from:
##www.kaggle.com/code/arjanso/reinforcement-learning-chess-1-policy-iteration#1.1-State-Evaluation


from os import environ
import numpy as np
import pandas as pd
import os
import inspect
import main
from RLC.move_chess.environment import Board
from RLC.move_chess.agent import Piece
from RLC.move_chess.learn import Reinforce

env = Board()
env.render()
env.visual_board

p = Piece(piece = 'king')
r = Reinforce(p, env)


print(inspect.getsource(r.evaluate_state))
r.agent.value_function.astype(int)
state = (0,0)
r.agent.value_function[0,0] = r.evaluate_state(state,gamma=1)

r.agent.value_function.astype(int)






##(Goal) Checkmate