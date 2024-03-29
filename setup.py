from setup_reqs import use_setuptools
use_setuptools()
import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "rl_lib_simple",
    version = "1.3",
    author = "JustaGist",
    author_email = "saifksidhik@gmail.com",
    description = ("library containing: 1. the gridworld environment and its visualizer for testing discrete reinforcement learning algorithms; 2. the contextual bandits environment and fully connected neural network for solving the problem."),
    license = "BSD",
    keywords = "reinforcement learning, q learning, sarsa, grid world, fully connected network, neural network, bandits, contextual bandits",
    url = "https://bitbucket.org/justagist/reinfor_learn",
    # packages=['rl_lib','envs','utils','alg_demos'],
    # packages=['rl_lib/envs', 'rl_lib/utils', 'rl_lib/alg_demos'],
    packages=find_packages(),
    scripts=['rl_lib_simple/commandscripts/qlearn-gridworld-gui'],
    # package_dir = {'envs':'rl_lib/envs', 'utils':'rl_lib/envs', 'alg_demos':'rl_lib/alg_demos'},
    install_requires=[
          'pygame', 'numpy'
      ],
    long_description=read('README.md'),
    classifiers=[],
    #     "Development Status :: 3 - Alpha",
    #     "Topic :: Utilities",
    #     "License :: OSI Approved :: BSD License",
    # ],
)