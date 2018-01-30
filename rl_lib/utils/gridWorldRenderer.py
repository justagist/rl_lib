''' Pygame render class for visualising GridWorld Environment (gridWorldEnv.py) 
    ---- for testing reinforcement learning algorihtms    

    @author: JustaGist (saifksidhik@gmail.com)
    @file: gridWorldRenderer.py
    @package: rl_lib v1.1
'''

from pygame.locals import *
import pygame, sys
import numpy as np


green = (40,255,30)
blue = (0,0,200)
red =  (155,20,30)
yellow = (255,255,0)
white = (255,255,255)
black = (0,0,0)

TRAP = 0
SAFE = 1
START = 2
TARGET = 3
AGENT = 4

colours = {
    TRAP: black,
    SAFE: white,
    START: blue,
    TARGET: green,
    AGENT: red
    }

TILESIZE = 50

clock = pygame.time.Clock()

# window.fill((255, 255, 255))
# tilemap (format - list of lists) =
#         [
#         [TRAP,SAFE,SAFE,SAFE, START],
#         [SAFE,START,SAFE,SAFE, SAFE],
#         [START, TRAP,SAFE,SAFE, START],
#         [START, TRAP,SAFE,SAFE, TRAP],
#         [SAFE,SAFE,SAFE,SAFE,TRAP]
#         ]

class GridWorldRenderer:

    def __init__(self, grid = None, rows = None, cols = None, start = None, goal = None, caption = 'Grid World - Reinforcement Learning'):

        if grid is not None: # initialise using grid. The other arguments are not required
            self._create_grid_world_from_matrix(grid)
        elif rows is not None and cols is not None and start is not None and goal is not None:
            self._create_grid_world_from_dimensions(rows,cols,start,goal)
        else:
            raise Exception("Grid cannot be created. Not enough information available.")

        self._setup_pygame_window(caption)

        self.running_ = True

    def _setup_pygame_window(self, caption):

        pygame.init()

        # ----- labels
        font=pygame.font.SysFont('liberationserif', 15)
        font.set_bold(True)
        self.start_text = font.render('START', True, black)
        self.goal_text = font.render('GOAL', True, black)

        # self.start_rect = pygame.get_rect(start_text)

        self.DISPLAYSURF = pygame.display.set_mode((self.map_width_*TILESIZE,self.map_height_*TILESIZE))
        pygame.display.set_caption(caption)
        

    def _create_grid_world_from_matrix(self, grid):

        self.tilemap_ = grid.tolist()
        self.map_width_ = grid.shape[1]
        self.map_height_ = grid.shape[0]

        # ----- finding coordinates of start grid and goal grid for labelling them
        start_tile_coord = np.where(grid==START)
        goal_tile_coord = np.where(grid==TARGET)

        # ----- defining rectangles around the labels for placing them in pygame window
        self.start_tile_rect = ((start_tile_coord[1][0])*TILESIZE, (start_tile_coord[0][0]+0.25)*TILESIZE, TILESIZE, TILESIZE)
        self.goal_tile_rect = ((goal_tile_coord[1][0]+0.1)*TILESIZE, (goal_tile_coord[0][0]+0.3)*TILESIZE, TILESIZE, TILESIZE)

    def _create_grid_world_from_dimensions(self, row, col, start, goal):

        self.tilemap_ = [[SAFE for i in range(col)] for j in range(row)]
        self.tilemap_[start[0]][start[1]] = START
        self.tilemap_[goal[0]][goal[1]] = TARGET
        self.map_width_ = col
        self.map_height_ = row

        self.start_tile_rect = ((start[1])*TILESIZE, (start[0]+0.25)*TILESIZE, TILESIZE, TILESIZE)
        self.goal_tile_rect = ((goal[1]+0.1)*TILESIZE, (goal[0]+0.3)*TILESIZE, TILESIZE, TILESIZE)

    def blit_text(self,surface, text, pos, font, color=pygame.Color('black')): # for displaying multiline text in pygame
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = surface.get_size()
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.

    def execute_collect_mouse_response(self):

        self.user_input_obstacles = []

        font=pygame.font.SysFont('liberationserif', 15)
        font.set_bold(True)
        instruction = 'Press Enter or click to begin. \nClose this window or press Enter again when done'

        user_agreed = False

        while not user_agreed:
            self.DISPLAYSURF.fill((20,20,20))

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.close()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        user_agreed = True

            self.blit_text(self.DISPLAYSURF, instruction, (self.map_width_*TILESIZE/4,self.map_height_*TILESIZE/4),font,white)
            pygame.display.update()


        while True:
            mouse_x = pygame.mouse.get_pos()[0]
            mouse_y = pygame.mouse.get_pos()[1]

            # print mouse_x, mouse_y

            # for event in pygame.event.get():
            #     if event.type == QUIT:
            #         pygame.quit()


            self.DISPLAYSURF.fill((0,0,0))
            for row in range(self.map_height_):
                # print            
                for col in range(self.map_width_):
                    color = colours[self.tilemap_[row][col]];
                    if mouse_x >= (col * TILESIZE) and mouse_x <= (col* TILESIZE) + TILESIZE:
                        if mouse_y >= (row * TILESIZE) and mouse_y <= (row* TILESIZE) + TILESIZE:
                            # print (str(row) + " " + str(col))
                            color = yellow;    

                            event = pygame.event.poll()
                            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                                self.close()
                                break
                                break
                                break
                            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # if clicked the grid becomes an obstacle, if clicked again, removes obstacle
                                if self.tilemap_[row][col] == SAFE:
                                    self.tilemap_[row][col] = TRAP
                                    self.user_input_obstacles.append((row,col))
                                elif self.tilemap_[row][col] == TRAP:
                                    self.tilemap_[row][col] = SAFE
                                    self.user_input_obstacles.remove((row,col))

                    pygame.draw.rect(self.DISPLAYSURF, color, (col*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE))

            self.DISPLAYSURF.blit(self.start_text, self.start_tile_rect)
            self.DISPLAYSURF.blit(self.goal_text, self.goal_tile_rect)
            pygame.display.update()


    def get_mouseclick_record(self):

        obstcls = self.user_input_obstacles
        self.user_input_obstacles = []

        if len(obstcls) > 0:
            return obstcls
        else:
            return None


    def execute_path_loop(self, path_coords):

        run = True

        while run:

            for tile in path_coords:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()

                self.DISPLAYSURF.fill((0,0,0));
                for row in range(self.map_height_):
                    # print            
                    for col in range(self.map_width_):
                        if (row,col) != tile:
                            color = colours[self.tilemap_[row][col]];
                        else:
                            color = colours[AGENT]
                            # self.DISPLAYSURF.blit(self.start_text, self.start_text.get_rect())
                        # if mouse_x >= (col * TILESIZE) and mouse_x <= (col* TILESIZE) + TILESIZE:
                        #     if mouse_y >= (row * TILESIZE) and mouse_y <= (row* TILESIZE) + TILESIZE:
                        #         print (str(row) + " " + str(col))
                        #         color = yellow;                                                                                                            
                        pygame.draw.rect(self.DISPLAYSURF, color, (col*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE))

                self.DISPLAYSURF.blit(self.start_text, self.start_tile_rect)
                self.DISPLAYSURF.blit(self.goal_text, self.goal_tile_rect)
                pygame.display.update()
                clock.tick(5)

        pygame.quit()


    def render(self, agent_pos):
        pygame.event.pump()
        self.DISPLAYSURF.fill((0,0,0));
        for row in range(self.map_height_):
            # print            
            for col in range(self.map_width_):
                if (row,col) != agent_pos:
                    color = colours[self.tilemap_[row][col]];
                else:
                    color = colours[AGENT]
                # if mouse_x >= (col * TILESIZE) and mouse_x <= (col* TILESIZE) + TILESIZE:
                #     if mouse_y >= (row * TILESIZE) and mouse_y <= (row* TILESIZE) + TILESIZE:
                #         print (str(row) + " " + str(col))
                #         color = yellow;                                                                                                            

                pygame.draw.rect(self.DISPLAYSURF, color, (col*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE))

        self.DISPLAYSURF.blit(self.start_text, self.start_tile_rect)
        self.DISPLAYSURF.blit(self.goal_text, self.goal_tile_rect)
        pygame.display.update()


    def close(self):
        pygame.quit()


if __name__ == '__main__':
    env = gridWorldEnv()

    cl = gridWorldRenderer(env._get_grid_world())

    cl.execute()
