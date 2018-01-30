''' 

Testing the library. Solve gridworld environment using Q-learning/Sarsa
--- for testing different action policies and knowledge updation
    

    @author: JustaGist (saifksidhik@gmail.com)
    @file: test_qlearn.py
    @package: rl_lib_simple v1.2

USAGE: python demo_qlearn.py 

'''

import sys
import numpy as np
from rl_lib_simple.envs.gridWorldEnv import GridWorldEnv
from rl_lib_simple.discreteQLearning import QLearnerDiscrete


def obtain_traps():

    n = raw_input("Number of traps?\n")

    if n == '':
        print "Give valid value"
        return obtain_traps()

    else:
        traps = []
        for i in range(int(n)):
            x = raw_input("Row coordinate of trap number %d\n"%i)
            y = raw_input("Column coordinate of trap number %d\n"%i)
            traps.append(int(x),int(y))
        return traps

if __name__ == '__main__':


    row = 6
    col = 7
    start_pos = (1,1)
    target = None
    list_of_traps = None
    render = True

    if len(sys.argv) == 2:
        render = bool(int(sys.argv[1]))

    if len(sys.argv) > 2:
        row = int(sys.argv[1])
        col = int(sys.argv[2])
        if len(sys.argv) > 3:
            render = bool(int(sys.argv[3]))

    print "\n\n*********** Reinforcement Learning Demo ***********\n\n"

    print "Grid World Details:\nRows: %d\tCols: %d"%(row,col)
    print "Start Position:", start_pos,"\tGoal Position:",(0,0)
    print "Traps: Random \tVisualise Learning:", render


    env = GridWorldEnv(grid_row = row, grid_col = col, start_pos = start_pos, list_of_hole_pos = list_of_traps, target = target, render = render)
    learner = QLearnerDiscrete(env)


    qtable = learner.find_best_q_table()

    print "Final Q-Table Values: "
    print qtable

    # act_path =  learner.find_best_actions_at_each_state()

    env.visualise_optimal_path(qtable)
