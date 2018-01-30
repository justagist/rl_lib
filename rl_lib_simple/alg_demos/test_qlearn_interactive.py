''' 

Interactive version to test the implementation for solving the gridworld environment using Q-learning/Sarsa
--- for testing different action policies and knowledge updation


    @author: JustaGist (saifksidhik@gmail.com)
    @file: test_qlearn_interactive.py
    @package: rl_lib_simple v1.2

USAGE: python test_qlearn_interactive.py 

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

    show = True
    row = col = 6
    start_pos = (0,0)
    target = None
    list_of_traps = None
    render = True

    print "\n\n*********** Reinforcement Learning Demo ***********\n\n"

    print "Grid World Details:\nRows: %d\tCols: %d"%(row,col)
    print "Start Position:", start_pos,"\tGoal Position:",(0,0)
    print "Traps: Random \tVisualise Learning: True"

    use_demo = raw_input("Use Default values?(Y/n)\n")
    if use_demo != 'y' and use_demo != 'Y' and use_demo != '':

        r = raw_input("No of rows in World? (6)\n")
        if r != '':
            row = int(r)

        c = raw_input("No of columnss in World? (6)\n")
        if c != '':
            col = int(c)

        start1 = raw_input("Starting Position (Row coordinate) (0)?\n")
        if start1 != '':
            start1 = int(r)
        else:
            start1 = 0

        start2 = raw_input("Starting Position (Column coordinate) (0)?\n")
        if start2 != '':
            start2 = int(r)
        else:
            start2 = 0

        start_pos = (start1,start2)

        target1 = raw_input("Goal Position (Row coordinate) (5)?\n")
        if target1 != '':
            target1 = int(r)

        target2 = raw_input("Goal Position (Column coordinate)? (5)\n")
        if target2 != '':
            target2 = int(r)

        target = (target1,target2) if (target1 != '' and target2 != '') else None

        list_ = raw_input("Random traps in world? (Y/n)\n")
        if list_ != 'y' and list_ != 'Y' and list_ != '':
            list_of_traps = obtain_traps()

        vis = raw_input("Visualise Learning Stage? (Y/n) (turn off for faster learning)\n")
        if vis != 'y' and vis != 'Y' and vis == '':
            render = False

    tgt = (row-1,col-1) if target is None else target

    print "Grid World Details:\nRows: %d\tCols: %d"%(row,col)
    print "Start Position:", start_pos,"\Goal Position:",tgt
    print "Traps: Random \tVisualise Learning: True"


    env = GridWorldEnv(grid_row = row, grid_col = col, start_pos = start_pos, list_of_hole_pos = list_of_traps, target = target, render = render)
    learner = QLearnerDiscrete(env)


    qtable = learner.find_best_q_table()

    print "Final Q-Table Values: "
    print qtable

    env.visualise_optimal_path(qtable)