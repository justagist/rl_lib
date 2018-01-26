import gym
from gym.utils import seeding
from gym import spaces
# from gym import utils
# import os, subprocess, time, signal
import numpy as np

# from gym_maze.envs.maze_view_2d import MazeView2D

class gridWorldEnv(gym.Env):

    def __init__(self, grid_row = 4, grid_col = 4, start_pos = (0,0), list_of_hole_pos = None, target = None):

        if list_of_hole_pos is None:
            if grid_row == 4 and grid_col == 4: # Similar to (4x4) FrozenLake Env
                list_of_hole_pos = [(1,1),(1,3),(2,3),(3,0)]
            else:
                list_of_hole_pos = [(int(grid_row/2),int(grid_col/2))]

        if target == None:
            target = (grid_row-1,grid_col-1)

        if start_pos not in list_of_hole_pos:
            start_pos = start_pos
        else:
            raise Exception("Start position is in a hole!!")

        self.traps = list_of_hole_pos

        self._seed()
        self._configure_environment(grid_row, grid_col, list_of_hole_pos, start_pos, target)

        self.obs_ = self.starting_state_
        # self._create_observation_space() # convert the grid world to 1D for easy creation of Q-table



    def _configure_environment(self,row,col,list_of_hole_pos, start_pos, target_pos):

        def _set_traps(grid, list_of_coordinates):

            row_list = []
            col_list = []
            for i,j in list_of_coordinates:
                row_list.append(i)
                col_list.append(j)

            grid[np.array(row_list),np.array(col_list)] = 0

            return grid


        grid = np.ones((row,col)) 

        self.grid_ = _set_traps(grid,list_of_hole_pos)

        self.obs_space_ = self.grid_.flatten()

        self.starting_state_ = self._convert_coords_to_obs(start_pos)

        self.target_state_ = self._convert_coords_to_obs(target_pos)

        # print self.obs_space_


        # self._env = spaces.Box(np.array([0,0]),np.array([4,4]))

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)

        return [seed]

    def _step(self, action):
        """

        Parameters
        ----------
        action : 0: left; 1: up; 2: right; 3: down (All are one step each)

        Returns
        -------
        ob, reward, episode_over, info : tuple
            ob (object) :
                an environment-specific object representing your observation of
                the environment.
            reward (float) :
                amount of reward achieved by the previous action. The scale
                varies between environments, but the goal is always to increase
                your total reward.
            episode_over (bool) :
                whether it's time to reset the environment again. Most (but not
                all) tasks are divided up into well-defined episodes, and done
                being True indicates the episode has terminated. (For example,
                perhaps the pole tipped too far, or you lost your last life.)
            info (dict) :
                 diagnostic information useful for debugging. It can sometimes
                 be useful for learning (for example, it might contain the raw
                 probabilities behind the environment's last state change).
                 However, official evaluations of your agent are not allowed to
                 use this for learning.
        """
        self._take_action(action)
        self.obs_ = self._get_observation()

        # reward = self._get_reward()
        # ob = self.env.getState()
        episode_over = ob == self._target
        # return ob, reward, episode_over, {}

    def _convert_coords_to_obs(self, coords): #(row,col)

        return coords[0]*self.grid_.shape[0] + coords[1]

    def _set_current_state(self,coords): #(row,col)
        '''
        set current state to the desired row and col, in the 1D obs_space_

        coords list: (desired_row, desired_col)
        '''

        self.obs_ = self._convert_coords_to_obs(coords)

    def _get_current_obs(self):

        return self.obs_

    def _get_grid_world(self):

        return self.grid_

    def _get_observation_space(self):

        return self.obs_space_

    def _get_coords_from_state(self, state):

        row = int(state/self.grid_.shape[1])
        col = state - (row * self.grid_.shape[1])

        return (row,col)

    def _reset(self):
        pass

    def _render(self, mode='human', close=False):
        pass

    def _take_action(self, action):

        if self.obs_ not in range(self.obs_space_.size): # sanity check
            raise Exception("current observation not in observation space!")
        
        if action == 0: # go left one step
            # if self.state_col > 0:
            #     self.state_col -=1
            if self.obs_%self.grid_.shape[1] != 0: # obs_ not in the leftmost column of the grid
                self.obs_ -= 1
            else:
                print "leftmost extreme"

        elif action == 1: # go up
            # if self.state_row > 0:
            #     self.state_row -=1
            if self.obs_ not in range(self.grid_.shape[1]): # obs_ not in the first row of the grid
                self.obs_ -= self.grid_.shape[1]
            else:
                print "topmost extreme"

        elif action == 2: # go right
            # if self.state_col < self.grid_.shape[1]-1:
            #     self.state_col +=1
            if (self.obs_+1)%self.grid_.shape[1] != 0: # obs_ not in the rightmost col of grid_
                self.obs_ += 1
            else:
                print "rightmost extreme"

        elif action == 3: # go down
            # if self.state_row < self.grid_.shape[0]-1:
            #     self.state_row +=1
            if self.obs_ > (self.obs_space_.size - 1 - self.grid_.shape[1]): # obs not in the last row of the grid
                self.obs_ += self.grid_.shape[1]
            else:
                print "bottommost extreme"

    def _get_reward(self):
        """ Reward is given for XY. """
        # if self.status == FOOBAR:
        #     return 1
        # elif self.status == ABC:
        #     return self.somestate ** 2
        # else:
        #     return 0



# class envSpaces(spaces.Discrete):



## ======================== ##
#         TEST CODE          #
## ======================== ##
if __name__ == '__main__':
    
    grid = gridWorldEnv()

    print grid._get_grid_world()

    print grid._get_observation_space()

    print grid._get_current_obs(), grid._get_coords_from_state(grid._get_current_obs())



    # space = spaces.Discrete(5)
    # print space
    # # x = space.sample()
    # print space.contains(4)

    # view = MazeView2D(maze_name="OpenAI Gym - Maze (%d x %d)" % maze_size,
    #                                     maze_size=5, screen_size=(640, 640))
    # maze_size = (10,10)

    # low = np.zeros(len(maze_size), dtype=int)
    # high =  np.array(maze_size, dtype=int) - np.ones(len(maze_size), dtype=int)
    # observation_space = spaces.Box(low, high)
    # # x = space.sample()
    # # print space.contains(x)
    # print observation_space
    # print high 
    # print low
