''' 

A class for implementing Qlearning on discrete state and action spaces.
Simple implementation for solving the gridworld environment using Q-learning/Sarsa
--- for testing different action policies and knowledge updation


    @author: JustaGist (saifksidhik@gmail.com)
    @file: discreteQLearning 
    @package: rl_lib_simple v1.2

USAGE: python discreteQLearning.py <row> <col> <visualize?>
        (or) 
       python discreteQLearning.py <visualize?>
                where visualize = 1 or 0

'''
    
import sys
import numpy as np
from rl_lib_simple.envs.gridWorldEnv import GridWorldEnv

class QLearnerDiscrete:

    def __init__(self, env, lr = .8, y = .95, eps = 2000, action_policy = 'epsilon', update_policy = 'q'):

        self.env = env
        # ----- Initialize table with all zeros
        self.Q = np.zeros([len(self.env.obs_space_),len(self.env.actions_)])
        # ----- Set learning parameters
        self.lr = lr # learning rate
        self.y = y # discount factor
        self.num_episodes = eps
        self.update_policy = update_policy
        self.action_policy = action_policy
        # ----- create lists to contain total rewards and steps per episode
        self.rList = []

        print "Environment Details:\nStates:", len(self.env.obs_space_),"\tActions:", len(self.env.actions_),"\nLearning Rate:",self.lr,"\nDiscount Factor:",self.y,"\tNumber of Episodes",self.num_episodes


    def find_best_q_table(self):
        
        for i in range(self.num_episodes):

            try:

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
                    # a = np.random.randint(0,len(self.env.actions_)) # ----- random action (epsilon)
                    a = self._choose_action(self.env.actions_, q_values_of_current_state =self.Q[s,:], decay_factor = (1./(i+1))) # the last two are only necessary if using 'epsilon_greedy' policy

                    # ----- Get new state and reward from environment
                    s1,r,d,_ = self.env.step(a) # d is the boolean that states whether the state has reached the target state

                    # ----- Update Q-Table with new knowledge
                    # self.Q[s,a] = self.Q[s,a] + self.lr*(r + self.y*np.max(self.Q[s1,:]) - self.Q[s,a]) # ----- Q-learning
                    # self.Q[s,a] = self.Q[s,a] + self.lr*(r + self.y*self.Q[s1,a] - self.Q[s,a]) # ----- Sarsa
                    self.Q[s,a] = self._update_table(self.Q[s,:], a, self.Q[s1,:], r)

                    rAll += r

                    s = s1
                    # print i, sfa, _
                    if d == True:
                        break
                # print self.Q

                self.rList.append(rAll)

            except KeyboardInterrupt:
                print "stopping learning"
                break

        self.env.close()

        return self.Q

    def reset_q_table(self):
        self.Q = np.zeros([self.env.observation_space.n,self.env.action_space.n])


    def find_best_actions_at_each_state(self):
        return self.Q.argmax(1)

    def _choose_action(self, actions, **kwargs):

        def epsilon(actions): 
            '''
            Given a list of possible actions, a random action is chosen unbiased
            '''
            return np.random.randint(0,len(actions))

        def epsilon_greedy(actions,q_values_of_current_state,decay_factor):
            '''
            Chooses action with maximum value (greedy). Noise is added to increase initial exploration. 
            decay_factor determines the influence of the noise over time. Choosing 1 would cause costant influence. Choose (1/(i+1)) to reduce the influence with increase in episode number i.
            q_values_of_current_state is the row in the QTable corresponding to the current state.
            '''      
            # a = np.argmax(self.Q[s,:] + np.random.randn(1,len(self.env.actions_))*(1./(i+1)))
            return np.argmax(q_values_of_current_state + np.random.randn(1,len(actions))*decay_factor)


        if self.action_policy == 'epsilon':

            return epsilon(actions)

        elif self.action_policy == 'epsilon_greedy':

            return epsilon_greedy(actions, **kwargs)

        else:
            raise Exception("Unknown Action Policy.")



    def _update_table(self, curr_state_qs, action, next_state_qs, reward):

        '''
        curr_state_qs = Q[s,:]
        next_state_qs = Q[s1,:]
        '''

        def update_using_q(curr_state_qs, action, next_state_qs, reward):
            # self.Q[s,a] = self.Q[s,a] + self.lr*(r + self.y*np.max(self.Q[s1,:]) - self.Q[s,a]) # ----- Q-learning alg
            return curr_state_qs[action] + self.lr*(reward + self.y*np.max(next_state_qs) - curr_state_qs[action])

        def update_using_sarsa(curr_state_qs, action, next_state_qs, reward):
            # self.Q[s,a] = self.Q[s,a] + self.lr*(r + self.y*self.Q[s1,a] - self.Q[s,a]) # ----- Sarsa
            return curr_state_qs[action] + self.lr*(reward + self.y*next_state_qs[action] - curr_state_qs[action])


        if self.update_policy == 'q':

            return update_using_q(curr_state_qs, action, next_state_qs, reward)

        elif self.update_policy == 'sarsa':

            return update_using_sarsa(curr_state_qs, action, next_state_qs, reward)

        else: 
            raise Exception("Unkonwn Value Update Policy")

        

## ======================== ##
#         TEST CODE          #
## ======================== ##
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

    env.visualise_optimal_path(qtable)
