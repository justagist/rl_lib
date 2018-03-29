import numpy as np

class ContextualBandit():
    def __init__(self, bandits = [[0.2,0,-0.0,-5],[0.1,-5,1,0.25],[-5,5,5,5]]):
        
        # ----- List out our bandits. By default, arms 4, 2, and 1 (respectively) are the most optimal.
        self.bandits_ = np.asarray(bandits)

        self.state_space_ = [i for i in range(self.bandits_.shape[0])] # ----- currently chosen bandit
        self.actions_ = [i for i in range(self.bandits_.shape[1])] # ----- currently chosen bandit
        
    def get_random_bandit(self):
        self.state_ = np.random.choice(self.state_space_) #Returns a random state for each episode.
        return self.state_

    def get_bandits(self):
        return self.bandits_
        
    def pull_arm(self,action, state = None):
        '''
            Pulls the specified arm of the specified bandit and returns the reward
        '''
        ## ===== Original version =======

        # arm_value = self.bandits_[self.state_,action]
        # # ----- Get a random number. This will be compared to the value of pulling the arm of the current bandit
        # result = np.random.randn(1)

        # if result > arm_value:
        #     return 1
        # else:
        #     return -1

        ## ==============================

        if state is None:
            state = self.state_

        arm_value = self.bandits_[state,action]

        return -arm_value

    def get_random_state(self):
        return self.get_random_bandit()

    def step(self, action):
        return None, self.pull_arm(action), None, None # ----- keeping format of Gym Env step function