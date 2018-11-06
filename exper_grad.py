from mancala import *
from minimax_1 import *
from nr import *

moves = 100
verbose = False
max_depth = [1,2,3,4,5,6,7,8]
list = [(2,1),(3,1),(3,2),(4,2),(5,3),(6,4)]
for x in list:
    mg = MancalaGame(size=x[0],count=x[1])
    state = mg.initial()
    for y in max_depth:
        _,_,nc = minimax_ab(mg,state,None,None,y)
        nc = nc -1
        alg = lambda game, state: minimax_ab(game, state, max_depth=y)
        fs_ab = play(mg, alg, moves=moves, verbose=verbose)
        print("ab: %f" % fs_ab)
        b0 = (nc + 1)**(1./y)
        b = newton(b0,g,dg,nc,y)
        print("branching factor:")
        print(b[-1])

