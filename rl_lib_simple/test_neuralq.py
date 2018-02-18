import gym
import numpy as np
import random
import tensorflow as tf
import matplotlib.pyplot as plt
from rl_lib_simple.envs.gridWorldEnv import GridWorldEnv

# env = gym.make('FrozenLake-v0')
env = GridWorldEnv(4,4, render = False)

# print env.take_random_action()
# print "here"

tf.reset_default_graph()

#These lines establish the feed-forward part of the network used to choose actions
inputs1 = tf.placeholder(shape=[1,16],dtype=tf.float32)
W = tf.Variable(tf.random_uniform([16,4],0,0.01))
Qout = tf.matmul(inputs1,W)
predict = tf.argmax(Qout,1)

#Below we obtain the loss by taking the sum of squares difference between the target and prediction Q values.
nextQ = tf.placeholder(shape=[1,4],dtype=tf.float32)
loss = tf.reduce_sum(tf.square(nextQ - Qout))
trainer = tf.train.GradientDescentOptimizer(learning_rate=0.1)
updateModel = trainer.minimize(loss)

init = tf.global_variables_initializer()

# Set learning parameters
y = .99
e = 0.1
num_episodes = 2000
#create lists to contain total rewards and steps per episode
jList = []
rList = []

# A tf session may own resources, such as variables, queues, and readers. It is important to release these resources when they are no longer required. To do this, either invoke the close() method on the session, or use the session as a context manager. The following methods are equivalent.
'''
# Using the `close()` method.
sess = tf.Session()
sess.run(...)
sess.close()

# Using the context manager.
with tf.Session() as sess:
  sess.run(...)

'''
with tf.Session() as sess:
    sess.run(init)
    testQ = np.zeros((16,4))
    for i in range(num_episodes):
        #Reset environment and get first new observation
        s = env.reset()
        rAll = 0
        d = False
        j = 0
        #The Q-Network
        print i
        while j < 99:
            j+=1
            #Choose an action by greedily (with e chance of random action) from the Q-network
            a,allQ = sess.run([predict,Qout],feed_dict={inputs1:np.identity(16)[s:s+1]})
            testQ[s,:] = allQ
            # print s,a, testQ
            # print a, allQ
            # raw_input()
            if np.random.rand(1) < e:
                # a[0] = env.action_space.sample()
                a[0] = env.take_random_action()
            #Get new state and reward from environment
            s1,r,d,_ = env.step(a[0])
            #Obtain the Q' values by feeding the new state through our network
            Q1 = sess.run(Qout,feed_dict={inputs1:np.identity(16)[s1:s1+1]})
            #Obtain maxQ' and set our target value for chosen action.
            maxQ1 = np.max(Q1)
            targetQ = allQ
            targetQ[0,a[0]] = r + y*maxQ1
            # print targetQ
            # raw_input()
            #Train our network using target and predicted Q values
            _,W1 = sess.run([updateModel,W],feed_dict={inputs1:np.identity(16)[s:s+1],nextQ:targetQ})
            # print nextQ
            # raw_input()
            rAll += r
            # s = s1
            s = env._get_current_state()
            if d == True:
                #Reduce chance of random action as we train the model.
                e = 1./((i/50) + 10)
                break
        jList.append(j)
        rList.append(rAll)

print testQ

print "Percent of succesful episodes: " + str(sum(rList)/num_episodes) + "%"

''' Neural trained Q-table preodictions

[[-2.63129878e+00 -1.90356026e+01  9.99981918e+01  9.76629868e+01]
 [-1.42750359e+00 -2.61309814e+00  9.99998474e+01  9.65411224e+01]
 [ 9.67097015e+01 -1.09881365e+00 -1.29615879e+00  1.00000076e+02]
 [ 9.55762711e+01  1.45523669e-03 -1.99928322e+01 -1.99945812e+01]
 [-1.32573948e+01 -5.70025826e+00  3.79073563e+01  9.26990509e+01]
 [ 0.00000000e+00  0.00000000e+00  0.00000000e+00  0.00000000e+00]
 [ 9.68824615e+01 -1.00023174e+00 -1.00007367e+00  1.00000092e+02]
 [ 0.00000000e+00  0.00000000e+00  0.00000000e+00  0.00000000e+00]
 [-1.39035673e+01  8.32314453e+01  8.55116959e+01 -1.91983395e+01]
 [-5.89186287e+00  4.16112289e+01 -9.24920883e+01  8.90207138e+01]
 [ 9.12338181e+01  1.00000076e+02 -1.00041938e+00 -1.00037813e+00]
 [ 0.00000000e+00  0.00000000e+00  0.00000000e+00  0.00000000e+00]
 [ 0.00000000e+00  0.00000000e+00  0.00000000e+00  0.00000000e+00]
 [-5.18447208e+00 -7.90251999e+01  1.00000198e+02 -3.49898767e+00]
 [-9.64274216e+01  1.00000092e+02 -1.16409516e+00 -1.37733853e+00]
 [ 0.00000000e+00  0.00000000e+00  0.00000000e+00  0.00000000e+00]]

'''



# plt.plot(rList)