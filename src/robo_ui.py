# import sys module
# originally proto_ui2.py, now stored in prototypes/proto_ui2.py
import pygame
import sys
import multiprocessing as mp
import numpy as np
import threading
from blink import blink_block, generateStimuliSquares
import time
import math


class UI:
    def __init__(self, useThreading:bool=False):
        # Constants to edit for desired processes
        self.isThreading = useThreading
        print("Threading: "+str(self.isThreading)) 
        self.FREQ = [5, 10.2, 14.4, 18.3]
        ########
        self.threadsOn = False
        self.notDesired = False
        self.locs = ()
        self.user_input = ''
        self._init_const()
        self._init_pygame()
        self._init_text()
        self.LSIZE = self.X // 5
        
        # Some metrics
        self.startTime = time.time()

    def _init_const(self):
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.DESIRED = ('i', 'j', 'k', 'l')
        self.ENDSCRN = (pygame.K_x, pygame.K_ESCAPE)
        self.PROMPT = 'Please enter a command (i/j/k/l):'
        self.WRONG = "Incorrect char inputted"

    def _init_pygame(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.X, self.Y = self.screen.get_size()
        self.base_font = pygame.font.Font(None, 32)

    def _init_text(self):
        # prompt text
        self.text_prompt = self.base_font.render(self.PROMPT, True, self.WHITE)
        self.prompt_rect = self.text_prompt.get_rect()
        self.prompt_rect.center = (self.X // 2, self.Y // 2 - (self.base_font.get_height()) * 2)

        # wrong arg text
        self.text_wrong = self.base_font.render(self.WRONG, True, self.WHITE)
        self.wrong_rect = self.text_wrong.get_rect()
        self.wrong_rect.center = (self.X // 2, (self.Y // 4) * 3)

        # user input text
        self.text_rect = pygame.Rect(0, 0, 0, 0)
        self.text_rect.center = (self.X // 2, self.Y // 2 - (self.base_font.get_height()) // 2)

        # black rect to cover/update text segment of screen
        self.black_rect = pygame.Rect(0, 0, self.prompt_rect.width, 0)
        self.black_rect.height = self.wrong_rect.top + self.base_font.get_height() - self.prompt_rect.top // 2
        self.black_rect.center = (self.X // 2, self.Y // 2)

    def start_threads(self):
        threads = {}
        for i in range(0, 4):
            threads[i] = threading.Thread(target=blink_block, args=([self.screen, self.FREQ[i], self.locs[i], self.LSIZE, i + 1]))
            threads[i].setDaemon(True)
            threads[i].start()

    def no_thread_stimuli(self, j):
        for i in range(0, len(self.FREQ)):
            result = math.sin(2 * math.pi * self.FREQ[i] * j / 60)
            sign = lambda x: (1, 0)[x < 0]
            color = 255 * sign(result)
            colors = [color, color, color]
            pose = self.locs[i]
            stimuli_rect = pygame.Rect(pose[0], pose[1], self.LSIZE, self.LSIZE)
            pygame.draw.rect(self.screen, colors, stimuli_rect)
            pygame.display.update()

    def box_names(self):
        labels = ['Forward', 'Back', 'Left', 'Right']
        for i in range(0, 4):
            label_text = self.base_font.render(labels[i], True, self.WHITE)
            label_rect = label_text.get_rect()
            if (i % 2) == 0:
                temploc = (self.locs[i][0]+self.LSIZE, self.locs[i][1])
                print(temploc)
                label_rect.topleft = temploc
            else:
                label_rect.topright = self.locs[i]
            self.screen.blit(label_text, label_rect)

    def set_locs(self):
        # locations of stimuli blocks (top left corners of each block)
        sub_coord_w = self.X - (30.0 + self.LSIZE)
        sub_coord_h = self.Y - (30.0 + self.LSIZE)
        loc1 = (30.0, 30.0)
        loc2 = (sub_coord_w, 30.0)
        loc3 = (30.0, sub_coord_h)
        loc4 = (sub_coord_w, sub_coord_h)
        self.locs = (loc1, loc2, loc3, loc4)
        #####

    def run_ui(self):
        user_text = ''
        self.screen.fill(self.BLACK)
        # local vars for non-threading stimuli
        change_time = 0
        delay = 1000./60
        show = True
        j = 0
        self.set_locs()
        self.box_names()
        while True:
            
            for event in pygame.event.get():

                # if user types QUIT then the screen will close
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key in self.ENDSCRN):
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.unicode in self.DESIRED:
                        self.user_input = event.unicode
                        user_text = ' ' + self.user_input + ' '
                        self.notDesired = False
                    else:
                        self.user_input = ''
                        user_text = ''
                        self.notDesired = True

            # it will set background color of screen
            text_surface = self.base_font.render(user_text, True, self.BLACK, self.WHITE)

            # Draw black rect around text area of screen
            pygame.draw.rect(self.screen, self.BLACK, self.black_rect)

            # render texts at positions
            self.screen.blit(text_surface, self.text_rect)
            self.screen.blit(self.text_prompt, self.prompt_rect)
            if self.notDesired:
                self.screen.blit(self.text_wrong, self.wrong_rect)

            # update portion of screen
            pygame.display.flip()

            # no more than 60 fps
            self.clock.tick(60)

            current_time = pygame.time.get_ticks()
            if not self.isThreading and current_time >= change_time: # If no threading
                change_time = current_time + delay
                show = not show
                self.no_thread_stimuli(j)
                pygame.display.update()
                j+=1
                # print("Time elapsed: "+str(float(time.time() - self.startTime)))
            elif self.isThreading and not self.threadsOn:
                self.threadsOn = True
                self.start_threads()


if __name__ == "__main__":
    protoUI = UI(useThreading=True)
    protoUI.run_ui()
