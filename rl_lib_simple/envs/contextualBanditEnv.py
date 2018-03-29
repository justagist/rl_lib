''' 

A contextual bandits class for testing a fully connected neural network in predicting the most rewarding arm for a bandit.


    @author: JustaGist (saifksidhik@gmail.com)
    @file: discreteQLearning 
    @package: rl_lib_simple v1.3
    
    For demo, run contextual_bandit_solver.py in alg_demos
    
'''

import numpy as np

class ContextualBandit():
    '''
        Creates a set of bandits with n number of arms. 
        Each bandit has different success probabilities for each arm, 
        and as such requires different actions to obtain the best result.

    '''
    def __init__(self, bandits = [[0.2,0,-0.0,-5],[0.1,-5,1,0.25],[-5,5,5,5]]): # ----- The lower the bandit number, more likely a positive reward will be obtained
        
        # ----- List out our bandits. By default, arms 4, 2, and 1 (respectively) are the most optimal.
        self.bandits_ = np.asarray(bandits)

        self.state_space_ = [i for i in range(self.bandits_.shape[0])] # ----- The indices of the bandits
        self.actions_ = [i for i in range(self.bandits_.shape[1])] # ----- The indices of the arms
        
    def get_random_bandit(self):
        self.state_ = np.random.choice(self.state_space_) #Returns a random state for each episode.
        return self.state_

    def get_bandits(self):
        return self.bandits_

    def get_best_action(self, bandit):
        '''
            Returns the index of the best arm for a given bandit
        '''
        return np.argmin(self.get_bandits()[bandit])
        
    def pull_arm(self,action, state = None):
        '''
             Generates a random number from a normal distribution with a mean of 0. 
             The lower the bandit number, the more likely a positive reward will be returned. 

        '''
        if state is None:
            state = self.state_

        arm_value = self.bandits_[state,action]
        # ----- Get a random number. This will be compared to the value of pulling the arm of the current bandit
        result = np.random.randn(1)

        if result > arm_value:
            return 1
        else:
            return -1


    def get_random_state(self):
        return self.get_random_bandit()

    def step(self, action):
        return None, self.pull_arm(action), None, None # ----- keeping format of Gym Env step function
