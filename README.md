# rl_lib_simple 

A repo for learning and testing RL algorithms.

* QLearning for discrete grid World
* Sarsa value update and Q update policies implemented
* Greedy and greedy-epsilon action policies available


## Version Log

### Version 1.3

* Contextual bandits environment added to environments.
* Policy Gradient using a fully connected neural network learner added to solve the problem of contextual bandits (demo included).
* Bug Fixes

### Version 1.2 

* GUI developed (command line script available).
    * Custumizable world.
        * Customizable grid size.
        * Obstacles can be set manually.
        * Start and goal positions can be chosen.
    * Action and Update policies can be selected.
    * Learning Parameters can be set.
    * Command line script developed.
* Visualisation fixes

### Version 1.1

* Implemented Sarsa update algorithm.
* Visualization using pygame. Visualizer library created.
* Interactive script implemented. Takes input values from terminal.
* Command line script developed for interactive script.
* Command line arguments can be used to give input values.
* Packaged to library with environment and visualizer modules.

### Version 1.0

* QLearning algorithm for simple grid world environment.
* Environments library created containing grid world environment.
* Greedy and Epsilon-greedy action policies implemented.


## Installation: 

Run:

    sudo python setup.py install

### Note:

If setup fails saying 'SDL' library is missing, install libsdl and try again. In Ubuntu, the requirements can be fulfilled by running:

    sudo apt-get install libsdl2-2.0
    sudo apt-get install libsdl2-dev


## Test:

Run GUI from command line:

    qlearn-gridworld-gui