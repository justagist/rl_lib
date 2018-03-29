import numpy as np
from rl_lib_simple.envs.contextualBanditEnv import ContextualBandit
import tensorflow as tf
import tensorflow.contrib.slim as slim


class FCNetLearner():

    def __init__(self, env, lr = 0.001, eps = 10000):
        
        self.env = env
        self.lr_ = lr
        self.eps_ = eps

        self.num_states = len(env.state_space_)
        self.num_actions = len(env.actions_)

        self._initialise_model()

    def _initialise_model(self):

        tf.reset_default_graph() #Clear the Tensorflow graph.

        self.state_in_= tf.placeholder(shape=[1],dtype=tf.int32)

        self._create_fc_network()
        
        self._define_loss_function()

        self.action_probs_ = tf.trainable_variables()[0] #The weights we will evaluate to look into the network.
        
    def _create_fc_network(self):
        '''
            Create a fully connected network from input to output. 

            input_layer size = num_states
            output_layer size = num_actions

        '''

        state_in_OH = slim.one_hot_encoding(self.state_in_,self.num_states) # ----- encode input as one-hot-vector

        output = slim.fully_connected(state_in_OH, self.num_actions, biases_initializer=None, activation_fn=tf.nn.sigmoid, weights_initializer=tf.ones_initializer()) # ----- This is a convenience function which gives a tensor (of size num_actions) after multiplying the input with a fully connected weight vector
        self.output_ = tf.reshape(output,[-1]) # ----- flatten the output

        self.chosen_action_ = tf.argmax(self.output_,0) # ----- index of the highest value in output

    def _define_loss_function(self):

        self.reward_holder_ = tf.placeholder(shape=[1],dtype=tf.float32)
        self.action_holder_ = tf.placeholder(shape=[1],dtype=tf.int32)

        responsible_weight = tf.slice(self.output_,self.action_holder_,[1])
        self.loss_ = -(tf.log(responsible_weight)*self.reward_holder_)

    def find_best_outputs(self): # ----- Training

        def define_optimiser():
            return tf.train.GradientDescentOptimizer(learning_rate=self.lr_).minimize(self.loss_)

        self.train_step_ = define_optimiser()


env = ContextualBandit() #Load the bandits.
myAgent = FCNetLearner(env, lr=0.001) #Load the agent.
myAgent.find_best_outputs()

total_episodes = 10000 #Set total number of episodes to train agent on.

total_reward = np.zeros([myAgent.num_states,myAgent.num_actions]) #Set scoreboard for bandits to 0.
e = 0.1 #Set the chance of taking a random action.

init = tf.initialize_all_variables()

# Launch the tensorflow graph
with tf.Session() as sess:
    sess.run(init)
    i = 0
    while i < total_episodes:
        curr_state = env.get_random_state() #Get a state from the environment.
        
        #Choose either a random action or one from our network.
        if np.random.rand(1) < e:
            action = np.random.randint(myAgent.num_actions)
        else:
            action = sess.run(myAgent.chosen_action_,feed_dict={myAgent.state_in_:[curr_state]})
        
        _, reward, _, _ = env.step(action) #Get our reward for taking an action given a bandit.
        
        #Update the network.
        feed_dict={myAgent.reward_holder_:[reward],myAgent.action_holder_:[action],myAgent.state_in_:[curr_state]}
        _,action_probs = sess.run([myAgent.train_step_,myAgent.action_probs_], feed_dict=feed_dict)
        
        #Update our running tally of scores.
        total_reward[curr_state,action] += reward
        if i % 500 == 0:
            print "Mean reward for each of the " + str(myAgent.num_states) + " bandits: " + str(np.mean(total_reward,axis=1))
        i+=1
for a in range(myAgent.num_states):
    print "The agent thinks action " + str(np.argmax(action_probs[a])+1) + " for bandit " + str(a+1) + " is the most promising...."
    if np.argmax(action_probs[a]) == np.argmin(env.get_bandits()[a]):
        print "...and it was right!"
    else:
        print "...and it was wrong!"