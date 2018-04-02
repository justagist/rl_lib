''' 

A Policy Gradient using Fully Connected Neural Network (2-layer) for learning simple state to action mapping by learning from rewards obtained due to an action taken at a state.  


    @author: JustaGist (saifksidhik@gmail.com)
    @file: gridWorldEnv.py
    @package: rl_lib_simple v1.3

    For demo, run contextual_bandit_solver.py in alg_demos

'''

import numpy as np

import tensorflow as tf
import tensorflow.contrib.slim as slim


class PolicyGradientNetwork():

    def __init__(self, env, lr = 0.001, eps = 10000, rand_action_chance = 0.1):
        
        self.env_ = env
        self.lr_ = lr
        self.eps_ = eps
        self.rand_chance_ = rand_action_chance # ----- The probability of taking a random action during the training process

        self.num_states = len(env.state_space_)
        self.num_actions = len(env.actions_) 

        self._initialise_model()

    def _initialise_model(self):

        tf.reset_default_graph() # ----- Clear the Tensorflow graph.

        self.state_in_= tf.placeholder(shape=[1],dtype=tf.int32)

        self._create_fc_network()
        
        self._define_loss_function()

        self.action_probs_ = tf.trainable_variables()[0] # ----- The weights we will evaluate to look into the network.
        
    def _create_fc_network(self):
        '''
            Create a fully connected network from input to output. 

            input_layer size = num_states
            output_layer size = num_actions

        '''

        state_in_OH = slim.one_hot_encoding(self.state_in_,self.num_states) # ----- encode input as one-hot-vector

        output = slim.fully_connected(state_in_OH, self.num_actions, biases_initializer=None, activation_fn=tf.nn.sigmoid, weights_initializer=tf.ones_initializer()) # ----- This is a convenience function which gives a tensor (of size num_actions) after multiplying the input with a fully connected weight vector

        # ----- flatten the output
        self.output_ = tf.reshape(output,[-1]) 

        self.chosen_action_ = tf.argmax(self.output_,0) # ----- index of the highest value in output

    def _define_loss_function(self):

        self.reward_holder_ = tf.placeholder(shape=[1],dtype=tf.float32)
        self.action_holder_ = tf.placeholder(shape=[1],dtype=tf.int32)

        responsible_weight = tf.slice(self.output_,self.action_holder_,[1])
        self.loss_ = -(tf.log(responsible_weight)*self.reward_holder_)

    def find_best_actions(self, verbose = False): # ----- The learning step

        def define_optimiser():
            return tf.train.GradientDescentOptimizer(learning_rate=self.lr_).minimize(self.loss_)

        self.train_step_ = define_optimiser()

        # ----- Set scoreboard for bandits to 0.
        total_reward = np.zeros([self.num_states,self.num_actions]) 

        init = tf.initialize_all_variables()


        # ----- Launch the tensorflow graph
        with tf.Session() as sess:

            sess.run(init)

            i = 0
            print "\nTraining..."

            while i < self.eps_:
                # ----- Get a state from the environment.
                curr_state = self.env_.get_random_state() 
                
                # ----- Choose either a random action or one from our network.
                if np.random.rand(1) < self.rand_chance_:
                    action = np.random.randint(self.num_actions)
                else:
                    action = sess.run(self.chosen_action_,feed_dict={self.state_in_:[curr_state]})
                
                # ----- Get our reward for taking an action given a bandit.
                _, reward, _, _ = self.env_.step(action) 
                
                # ----- Update the network.
                feed_dict={self.reward_holder_:[reward],self.action_holder_:[action],self.state_in_:[curr_state]}
                _,action_probs, loss = sess.run([self.train_step_, self.action_probs_, self.loss_], feed_dict=feed_dict)
                
                # ----- Update our running tally of scores.
                total_reward[curr_state,action] += reward
                if verbose and (i+1) % 500 == 0:
                    print "\nTraining: {0:.0f}%".format(float((i+1)/float(self.eps_))*100),"Mean reward for each of the " + str(self.num_states) + " bandits: " + str(np.mean(total_reward,axis=1))
                    print "     Loss in state " + str(curr_state+1) + " = " + str(loss)
                i+=1
            print " "

        return action_probs