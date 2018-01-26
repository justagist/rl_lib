import numpy as np

class gridWorldEnv():

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

        # self._seed()
        self._configure_environment(grid_row, grid_col, list_of_hole_pos, start_pos, target)

        self.prev_state_ = self.state_ = self.starting_state_

        self.episode_done_ = False

        # self._create_observation_space() # convert the grid world to 1D for easy creation of Q-table

    ''' LIST OF CLASS VARIABLES: (self.)
        - state_            (int)           :current state (0 to size(grid world))
        - grid_             (np.array)      :grid_world with 1 for safe places, 0 for unsafe (traps)
        - obs_space_    
        - traps_
        - starting_state_
        - target_state_
        - actions_
        - episode_done_
        - status_
        - reward_

        TODO...

    '''


    def _configure_environment(self,row,col,list_of_hole_pos, start_pos, target_pos):

        def _set_traps_and_target(grid, list_of_coordinates, target):

            grid = self._set_traps_in_grid(grid, list_of_coordinates)

            grid = self._set_target_in_grid(grid, target)

            return grid


        grid = np.ones((row,col)) 

        self.grid_ = _set_traps_and_target(grid,list_of_hole_pos, target_pos)

        self.obs_space_ = self.grid_.flatten() # observation space. The state space will be the indices of the obs_space, i.e, [i for i in range(len(self.obs_space_))]

        self._set_starting_state(start_pos)

        self._set_target_state(target_pos)

        self.traps_ = [self._convert_coords_to_state(i) for i in list_of_hole_pos]

        self.safe_states_ = [i for i in range(len(self.obs_space_)) if self.obs_space_[i] == 1]
        # print self.obs_space_
        
        self.actions_ = {
        'left'  :   0,
        'up'    :   1,
        'right' :   2,
        'down'  :   3
        }

        # self._env = spaces.Box(np.array([0,0]),np.array([4,4]))

    def _set_traps_in_grid(self, grid, list_of_coordinates):
        
        row_list = []
        col_list = []
        for i,j in list_of_coordinates:
            row_list.append(i)
            col_list.append(j)

        grid[np.array(row_list),np.array(col_list)] = 0

        return grid

    def _set_target_in_grid(self, grid, target):

        grid[target] = 5
        return grid


    def _seed(self, seed=None):
        raise Exception("Not Implemented")

    def step(self, action = None):
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

        self._sanity_check()

        self.episode_done_ = False
        # ------- update self.state_ by taking some action
        if action is None:
            self.take_random_action()
        else:
            self._take_action(action)

        self.status_ = self._get_state_status()

        self.reward_ = self._compute_reward()

        step_details = {
        'prev state': self.prev_state_,
        'action'    : action,
        'status'    : self.status_
        }

        self.prev_state_ = self.state_

        return self.state_, self.reward_, self.episode_done_, step_details

        # return ob, reward, episode_over, {}

    def _convert_coords_to_state(self, coords): #(row,col)
        return coords[0]*self.grid_.shape[0] + coords[1]

    def _set_current_state(self,coords): #(row,col)
        self.state_ = self._convert_coords_to_state(coords)

    def _set_starting_state(self, coords):
        self.starting_state_ = self._convert_coords_to_state(coords)

    def _set_target_state(self, coords):
        self.target_state_ = self._convert_coords_to_state(coords)

    def _get_current_state(self):
        return self.state_

    def _get_current_observation(self):
        return self._get_observation_at(self.state_)

    def _get_observation_at(self,state):
        return self.obs_space_[state]

    def _get_grid_world(self):
        return self.grid_

    def _get_observation_space(self):
        return self.obs_space_

    def _convert_state_to_coords(self, state):

        row = int(state/self.grid_.shape[1])
        col = state - (row * self.grid_.shape[1])

        return (row,col)

    def reset(self, randomise = False):

        if randomise:
            self.starting_state_ = np.random.randint(0,len(self.safe_states_))

        self.state_ = self.starting_state_
        return self.state_

    def render(self, mode='human', close=False):
        pass

    def take_random_action(self):

        action = np.random.randint(0,len(self.actions_))
        self._take_action(action)

    def _sanity_check(self):

        if self.state_ not in range(self.obs_space_.size): # sanity check
            raise Exception("current observation not in observation space!")

    def _take_action(self, action):

        if isinstance(action, basestring):
            if action in self.actions_:
                action = self.actions_[action]
            else:
                raise Exception("Unrecognized Action Requested!")

        # print "taking action", action, [key for key, value in self.actions_.iteritems() if value == action][0]        

        if action == 0: # go left one step
            if self.state_%self.grid_.shape[1] != 0: # state_ not in the leftmost column of the grid
                self.state_ -= 1
            # else:
            #     print "leftmost extreme"

        elif action == 1: # go up
            if self.state_ not in range(self.grid_.shape[1]): # state_ not in the first row of the grid
                self.state_ -= self.grid_.shape[1]
            # else:
            #     print "topmost extreme"

        elif action == 2: # go right
            if (self.state_+1)%self.grid_.shape[1] != 0: # state_ not in the rightmost col of grid_
                self.state_ += 1
            # else:
            #     print "rightmost extreme"

        elif action == 3: # go down
            if self.state_ < (self.obs_space_.size - self.grid_.shape[1]): # obs not in the last row of the grid
                self.state_ += self.grid_.shape[1]
            # else:
            #     print "bottommost extreme"

        self._sanity_check()

    def _get_state_status(self,state = None):

        if state == None:
            state = self.state_

        if state == self.target_state_ and self._get_observation_at(state) == 5:
            self.episode_done_ = True
            return "target"

        elif self._get_observation_at(state) == 1:
            return "safe"

        elif self._get_observation_at(state) == 0:
            self.episode_done_ = True               # --- This can be commented out to get more exploration
            return "trap"
        else:
            raise Exception("ERROR: Unknown State Status")


    def _compute_reward(self, status = None):

        if status == None:
            status = self.status_

        if status == "trap":
            return -100

        if status == "target":
            return 1000

        if status == "safe":
            return 0


# class envSpaces(spaces.Discrete):



## ======================== ##
#         TEST CODE          #
## ======================== ##
if __name__ == '__main__':
    
    grid = gridWorldEnv()

    # print grid._get_grid_world()

    print grid._get_observation_space()

    print grid.safe_states_

    # print grid._get_current_state(), grid._convert_state_to_coords(grid._get_current_state())

    # grid._set_current_state((0,2))

    # print grid._get_current_state(), grid._convert_state_to_coords(grid._get_current_state())
    # grid._take_random_action()
    # grid._take_action('right')



    # grid._take_action('left')
    # print type(grid.actions_)



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
