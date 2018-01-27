''' Simple implementation for solving the gridworld environment using Q-learning/Sarsa
    --- for testing different action policies and knowledge updation
    

    @author: JustaGist (saifksidhik@gmail.com)
    @file: discrete_q_learning v1.1
    @package: rl_lib

    USAGE: python discrete_q_learning.py <row> <col> <visualize?>
            (or) 
           python discrete_q_learning.py <visualize?>
                    where visualize = 1 or 0
'''
    
import sys
import numpy as np
from rl_lib.envs.gridWorldEnv import gridWorldEnv

class QLearnerDiscrete:

    def __init__(self, env, lr = .8, y = .95, eps = 2000):

        self.env = env
        # ----- Initialize table with all zeros
        self.Q = np.zeros([len(self.env.obs_space_),len(self.env.actions_)])
        # ----- Set learning parameters
        self.lr = lr # learning rate
        self.y = y # discount factor
        self.num_episodes = eps
        # ----- create lists to contain total rewards and steps per episode
        self.rList = []

        print "Environment Details:\nStates:", len(self.env.obs_space_),"\tActions:", len(self.env.actions_),"\nLearning Rate:",self.lr,"\nDiscount Factor:",self.y,"\tNumber of Episodes",self.num_episodes


    def find_best_q_table(self):
        
        for i in range(self.num_episodes):

            # ----- Reset environment and get first new observation
            s = self.env.reset(randomise = True)
            # print s
            rAll = 0
            d = False
            j = 0
            sfa = s
            # ----- learning algorithm
            while j < 99:
                j+=1

                # ----- Choose an action 
                # a = np.argmax(self.Q[s,:] + np.random.randn(1,len(self.env.actions_))*(1./(i+1))) # ----- action with max(Q) and some noise which reduces over time (greedy - epsilon)
                a = np.random.randint(0,len(self.env.actions_)) # ----- random action (epsilon)

                # ----- Get new state and reward from environment
                s1,r,d,_ = self.env.step(a) # d is the boolean that states whether the state has reached the target state

                # ----- Update Q-Table with new knowledge
                self.Q[s,a] = self.Q[s,a] + self.lr*(r + self.y*np.max(self.Q[s1,:]) - self.Q[s,a]) # ----- Q-learning
                # self.Q[s,a] = self.Q[s,a] + self.lr*(r + self.y*self.Q[s1,a] - self.Q[s,a]) # ----- Sarsa

                rAll += r

                s = s1
                # print i, sfa, _
                if d == True:
                    break
            # print self.Q

            self.rList.append(rAll)

        self.env.close()

        return self.Q

    def reset_q_table(self):
        self.Q = np.zeros([self.env.observation_space.n,self.env.action_space.n])


    def find_best_actions_at_each_state(self):
        return self.Q.argmax(1)
        


if __name__ == '__main__':

    show = True
    row = col = 4

    if len(sys.argv) == 2:
        show = bool(int(sys.argv[1]))

    if len(sys.argv) > 2:
        row = int(sys.argv[1])
        col = int(sys.argv[2])
        if len(sys.argv) > 3:
            show = bool(int(sys.argv[3]))

    env = gridWorldEnv(row, col, render = show)
    learner = QLearnerDiscrete(env)


    qtable = learner.find_best_q_table()

    print "Final Q-Table Values: "
    print qtable

    # act_path =  learner.find_best_actions_at_each_state()

    env.visualise_optimal_path(qtable)
