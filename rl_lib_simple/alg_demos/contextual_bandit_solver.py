''' 

Testing the library. Solve contextual bandit environment using fully connected neural network performing policy gradients.

    @author: JustaGist (saifksidhik@gmail.com)
    @file: contextual_bandit_solver.py
    @package: rl_lib_simple v1.3

USAGE: python contextual_bandit_solver.py 

'''
from rl_lib_simple.envs.contextualBanditEnv import ContextualBandit
from rl_lib_simple.learners.policyGradientNetwork import PolicyGradientNetwork
import numpy as np

if __name__ == '__main__':
        
    # ----- Load the bandits
    env = ContextualBandit([[-5,1,0.1,2],[1,-5,3,5],[1,3,-5,4],[0.1,0.1,0.3,-4]]) 

    # ----- Load the agent
    learner = PolicyGradientNetwork(env, lr = 0.001, eps = 10000, rand_action_chance = 0.1) 

    # ----- Learning step
    action_probs = learner.find_best_actions(verbose = True)

    for bandit in range(learner.num_states):
        print "The agent thinks action " + str(np.argmax(action_probs[bandit])+1) + " for bandit " + str(bandit+1) + " is the most promising...."
        if np.argmax(action_probs[bandit]) == env.get_best_action(bandit):
            print "     ...and it was right!\n"
        else:
            print "     ...and it was WRONG!!\n"