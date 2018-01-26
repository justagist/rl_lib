''' Simple implementation for solving the gridworld environment using Q-learning/Sarsa
    --- for testing different action policies and knowledge updation

    (Based on tutorial at medium.com)
'''
    
import sys
import gym
import numpy as np
from gridWorldEnv import gridWorldEnv




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
                # self.Q[s,a] = self.Q[s,a] + self.lr*(r + self.y*np.max(self.Q[s1,:]) - self.Q[s,a]) # ----- Q-learning
                self.Q[s,a] = self.Q[s,a] + self.lr*(r + self.y*self.Q[s1,a] - self.Q[s,a]) # ----- Sarsa

                rAll += r

                s = s1
                # print i, sfa, _
                if d == True:
                    break
            # print self.Q

            self.rList.append(rAll)


        print "Optimum QTable obtained.\nScore over time: " +  str(sum(self.rList)/self.num_episodes)


    def reset_q_table(self):

        self.Q = np.zeros([self.env.observation_space.n,self.env.action_space.n])

    def get_q_table(self):

        return self.Q


if __name__ == '__main__':

    learner = QLearnerDiscrete(env = gridWorldEnv())

    learner.find_best_q_table()

    print "Final Q-Table Values"
    print learner.get_q_table()