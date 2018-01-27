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
brown = (40,60,90)
red =  (155,20,30)
yellow = (0,155,155)
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
    START: yellow,
    TARGET: green,
    AGENT: red
    }

TILESIZE = 50

clock = pygame.time.Clock()

# tilemap (format - list of lists) =
#         [
#         [TRAP,SAFE,SAFE,SAFE, START],
#         [SAFE,START,SAFE,SAFE, SAFE],
#         [START, TRAP,SAFE,SAFE, START],
#         [START, TRAP,SAFE,SAFE, TRAP],
#         [SAFE,SAFE,SAFE,SAFE,TRAP]
#         ]

class gridWorldRenderer:

    def __init__(self, grid):

        self._create_grid_world(grid)

        self._setup_pygame_window()

        self.running_ = True

    def _setup_pygame_window(self):

        pygame.init()
        self.DISPLAYSURF = pygame.display.set_mode((self.map_width_*TILESIZE,self.map_height_*TILESIZE))

        pygame.display.set_caption('Grid World - Reinforcement Learning')
        

    def _create_grid_world(self, grid):

         self.tilemap_ = grid.tolist()
         self.map_width_ = grid.shape[1]
         self.map_height_ = grid.shape[0]
         # print self.tilemap_

    def _cleanup(self):
        pygame.quit()

    def execute(self):


        while True:
            # mouse_x = pygame.mouse.get_pos()[0]
            # mouse_y = pygame.mouse.get_pos()[1]

            # print mouse_x, mouse_y

            # for event in pygame.event.get():
            #     if event.type == QUIT:
            #         pygame.quit()

            self.DISPLAYSURF.fill((0,0,0));
            for row in range(self.map_height_):
                # print            
                for col in range(self.map_width_):
                    color = colours[self.tilemap_[row][col]];
                    # if mouse_x >= (col * TILESIZE) and mouse_x <= (col* TILESIZE) + TILESIZE:
                    #     if mouse_y >= (row * TILESIZE) and mouse_y <= (row* TILESIZE) + TILESIZE:
                    #         print (str(row) + " " + str(col))
                    #         color = yellow;                                                                                                            

                    pygame.draw.rect(self.DISPLAYSURF, color, (col*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE))


            pygame.display.update()

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
                        # if mouse_x >= (col * TILESIZE) and mouse_x <= (col* TILESIZE) + TILESIZE:
                        #     if mouse_y >= (row * TILESIZE) and mouse_y <= (row* TILESIZE) + TILESIZE:
                        #         print (str(row) + " " + str(col))
                        #         color = yellow;                                                                                                            

                        pygame.draw.rect(self.DISPLAYSURF, color, (col*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE))


                clock.tick(5)
                pygame.display.update()

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


        pygame.display.update()


    def close(self):
        pygame.quit()


if __name__ == '__main__':
    env = gridWorldEnv()

    cl = gridWorldRenderer(env._get_grid_world())

    cl.execute()
