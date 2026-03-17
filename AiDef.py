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
print(inspect.getsource(r.evaluate_policy))
r.evaluate_policy(gamma=1)
r.agent.value_function.astype(int)
eps=0.1
k_max = 1000
value_delta_max = 0
gamma = 1
synchronous=True
value_delta_max = 0
for k in range(k_max):
    r.evaluate_policy(gamma=gamma,synchronous=synchronous)
    value_delta = np.max(np.abs(r.agent.value_function_prev - r.agent.value_function))
    value_delta_max = value_delta
    if value_delta_max < eps:
        print('converged at iter',k)
        break
r.agent.value_function.astype(int)
print(inspect.getsource(r.improve_policy))
print(inspect.getsource(r.policy_iteration))
r.policy_iteration()
agent = Piece(piece='king')
r = Reinforce(agent,env)
r.policy_iteration(gamma=1,synchronous=False)
r.agent.value_function.astype(int)
agent = Piece(piece='rook')  # Let's pick a rook for a change.
r = Reinforce(agent,env)
r.policy_iteration(k=1,gamma=1)  # The only difference here is that we set k_max to 1.

##(Goal) Checkmate