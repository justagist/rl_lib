''' GridWorld Environment Class (based on OpenAI Gym environments) for testing reinforcement learning algorihtms    

    @author: JustaGist (saifksidhik@gmail.com)
    @file: gridWorldEnv.py
    @package: reinforcement_learn
'''

import numpy as np
from utils.gridWorldRenderer import gridWorldRenderer

# ----- VALUES IN GRID:
TRAP = 0
SAFE = 1
START = 2
TARGET = 3
CURRENT = 4

TRAP_REWARD = -100
GOAL_REWARD = 100
SAFE_REWARD = 1
OUT_OF_BOUNDS_REWARD = -100

class gridWorldEnv():

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


    def __init__(self, grid_row = 4, grid_col = 4, start_pos = (0,0), list_of_hole_pos = None, target = None, render = False):

        if target == None:
            target = (grid_row-1,grid_col-1)

        if list_of_hole_pos is None:
            if grid_row == 4 and grid_col == 4: # Similar to (4x4) FrozenLake Env
                list_of_hole_pos = [(1,1),(1,3),(2,3),(3,0)]
            else:
                list_of_hole_pos = self._generate_random_traps(grid_row,grid_col,start_pos,target)

        print start_pos


        if start_pos in list_of_hole_pos or target in list_of_hole_pos:
            raise Exception("Starting position or target is in a hole!!")

        # self._seed()
        self._configure_environment(grid_row, grid_col, list_of_hole_pos, start_pos, target)

        self.prev_state_ = self.state_ = self.starting_state_
        self.variable_start_state_ = False # ----- will be set to true if the reset() function is called with random=True

        self.render_ = render

        if self.render_:
            self.visualizer_ = gridWorldRenderer(self.grid_)

        print "this ", self.starting_state_

        self.episode_done_ = False

    def _generate_random_traps(self,row,col,strt,tgt,ratio = 0.25):

        trap_rows = np.random.randint(row, size=int(row*col*ratio))
        trap_cols = np.random.randint(col, size=int(row*col*ratio))
        print [(i,j) for i,j in zip(trap_rows,trap_cols) if strt != (i,j) and tgt != (i,j)]
        return [(i,j) for i,j in zip(trap_rows,trap_cols) if strt != (i,j) and tgt != (i,j)]


    def _configure_environment(self,row,col,list_of_hole_pos, start_pos, target_pos):

        def _setup_grid_world(grid, list_of_coordinates, start, target):

            grid = self._set_traps_in_grid(grid, list_of_coordinates)

            grid = self._set_target_in_grid(grid, target)

            grid = self._set_start_pos_in_grid(grid, start)

            return grid

        print "val:", TRAP
        grid = np.full((row,col),SAFE) 

        self.grid_ = _setup_grid_world(grid,list_of_hole_pos,start_pos, target_pos)

        self.obs_space_ = self.grid_.flatten() # ----- observation space flattened for reducing dimensionality. The state space will be the indices of the obs_space, i.e, [i for i in range(len(self.obs_space_))]

        self.state_space_ = [i for i in range(len(self.obs_space_))]

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

        grid[np.array(row_list),np.array(col_list)] = TRAP

        return grid

    def _set_target_in_grid(self, grid, target):

        grid[target] = TARGET
        return grid

    def _set_start_pos_in_grid(self, grid, start):

        grid[start] = START
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
        state, reward, episode_done_, info : tuple
            state (int) :
                represents state/observation of
                the environment.
            reward (float) :
                amount of reward achieved by the previous action. The scale
                varies between environments, but the goal is always to increase
                your total reward.
            episode_done_ (bool) :
                whether it's time to reset the environment again. Most (but not
                all) tasks are divided up into well-defined episodes, and done
                being True indicates the episode has terminated. (For example,
                perhaps the pole tipped too far, or you lost your last life.)
            info (dict) :
                 diagnostic information useful for debugging.

        """

        self._sanity_check()

        self.episode_done_ = False
        # ------- update self.state_ by taking some action
        if action is None:
            self.take_random_action()
        else:
            self._take_action(action)

        # print "this", self.state_, self.prev_state_, action, self._convert_state_to_coords(self.prev_state_), self._convert_state_to_coords(self.state_)
        # print self.grid_

        self.status_ = self._get_state_status()

        self.reward_ = self._compute_reward()

        step_details = {
        'prev state': self.prev_state_,
        'action'    : action,
        'status'    : self.status_
        }

        if self.render_:

            self._render()

        self.prev_state_ = self.state_

        return self.state_, self.reward_, self.episode_done_, step_details

        # return ob, reward, episode_done_, {}

    def _render(self, mode = 'human'):

        self.visualizer_.render(self._convert_state_to_coords(self._get_current_state()))

    def _convert_coords_to_state(self, coords): #(row,col)
        return coords[0]*self.grid_.shape[1] + coords[1]

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
            self.variable_start_state_ = True
            self.starting_state_ = np.random.randint(0,len(self.safe_states_))

        self.state_ = self.starting_state_
        return self.state_

    def take_random_action(self):

        action = np.random.randint(0,len(self.actions_))
        self._take_action(action)

    def _sanity_check(self):

        if self.state_ not in range(self.obs_space_.size): # sanity check
            raise Exception("current observation not in observation space!")

    def _take_action(self, action): # ----- the action might take the agent out of bounds. This will be punished later in the _compute_reward function

        if isinstance(action, basestring):
            if action in self.actions_:
                action = self.actions_[action]
            else:
                raise Exception("Unrecognized Action Requested!")

        # print "taking action", action, [key for key, value in self.actions_.iteritems() if value == action][0]        
        self.state_ = self._transition(self.state_, action)

    def _transition(self, state, action):

        if action == 0: # go left one step
            if state%self.grid_.shape[1] != 0: # state_ not in the leftmost column of the grid
                state -= 1
            else:
                state = -5

        elif action == 1: # go up
            if self.state_ not in range(self.grid_.shape[1]): # state_ not in the first row of the grid
                state -= self.grid_.shape[1]
            else:
                state = -5

        elif action == 2: # go right
            if (self.state_+1)%self.grid_.shape[1] != 0: # state_ not in the rightmost col of grid_
                state += 1
            else:
                state = -5

        elif action == 3: # go down
            if self.state_ < (self.obs_space_.size - self.grid_.shape[1]): # obs not in the last row of the grid
                state += self.grid_.shape[1]
            else:
                state = -5

        return state


    def _get_state_status(self,state = None):

        if state == None:
            state = self.state_

        if state not in self.state_space_: # ----- the action took the agent out of the world. The agent is put back to previous state for q-table
            self.state_ = self.prev_state_
            self.episode_done_ = True
            return "out_of_bounds"

        elif state == self.target_state_ and self._get_observation_at(state) == TARGET:
            self.episode_done_ = True
            return "target"

        elif self._get_observation_at(state) == SAFE or self._get_observation_at(state) == START:
            return "safe"

        elif self._get_observation_at(state) == TRAP:
            self.episode_done_ = True               # --- This can be commented out to get more exploration
            return "trap"
        else:
            # print "STATE IS:", state, self.target_state_, self.test
            raise Exception("ERROR: Unknown State Status")


    def _compute_reward(self, status = None):

        if status == None:
            status = self.status_

        if status == "out_of_bounds":
            return OUT_OF_BOUNDS_REWARD

        if status == "trap":
            return TRAP_REWARD

        if status == "target":
            return GOAL_REWARD

        if status == "safe":
            return SAFE_REWARD

    def close(self):

        if self.render_:
            self.visualizer_.close()

    def visualise_optimal_path(self, Qtable):

        optimal_path = self._get_optimal_path(Qtable)

        if optimal_path is not None:
            self.visualizer_ = gridWorldRenderer(self.grid_)
            self.visualizer_.execute_path_loop(optimal_path)
        else:
            print "Best path could not be found!"


    def _get_optimal_path(self, Qtable, grid_space = True): 
        '''
        Computes the best path when the Qtable is given

        grid_space (bool): if True, returns array in grid coordinates. Otherwise in state space.
        '''

        def find_valid_optimum_transition(from_state, action_ratings):

            try:

                best_action = action_ratings.argmax()
                new_state = self._transition(from_state, best_action)

                action_validity = self._get_state_status(new_state)

                if action_validity == "safe" or action_validity == "target":
                    return new_state

                else:
                    action_ratings = np.array([action_ratings[i] for i in range(len(action_ratings)) if i != best_action])
                    return find_valid_optimum_transition(from_state, action_ratings)
            except ValueError():
                print "Valid path could not be found"
                sys.exit()


        optimal_path = []

        if self.variable_start_state_:
            self.starting_state_ = 0
        idx = self.starting_state_

        while idx != self.target_state_:
            print self._convert_state_to_coords(idx),
            optimal_path.append(idx)

            action_values_at_state = Qtable[idx]
            
            new_state = find_valid_optimum_transition(idx, action_values_at_state)

            idx = new_state
            
            '''
            best_action = action_values_at_state.argmax()
            idx = self._transition(idx, best_action)
            '''

            if len(optimal_path) > len(self.state_space_): # Optimal path could not be found
                return None

        optimal_path.append(self.target_state_)
        if grid_space:
            return [self._convert_state_to_coords(i) for i in optimal_path]

        return optimal_path


## ======================== ##
#         TEST CODE          #
## ======================== ##
if __name__ == '__main__':
    
    grid = gridWorldEnv(grid_row = 5, grid_col = 6, start_pos = (0,0), list_of_hole_pos = None, target = None)

    print grid._get_grid_world()

    print grid._get_observation_space()
