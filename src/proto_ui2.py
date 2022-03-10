# import sys module
import pygame
import sys
import multiprocessing as mp
import numpy as np
import threading
from blink import blink_block, generateStimuliSquares
import time


class UI:
    def __init__(self):
        self.threadsOn = False
        self.notDesired = False
        self._init_const()
        self._init_pygame()
        self._init_text()
        self.LSIZE = self.X // 4

    def _init_const(self):
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.DESIRED = ('i', 'j', 'k', 'l')
        self.ENDSCRN = (pygame.K_x, pygame.K_ESCAPE)
        self.PROMPT = 'Please enter a command (i/j/k/l):'
        self.WRONG = "Incorrect char inputted"
        self.FREQ = [1, 5, 10, 20]

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
        self.user_input = ''
        self.text_rect = pygame.Rect(0, 0, 0, 0)
        self.text_rect.center = (self.X // 2, self.Y // 2 - (self.base_font.get_height()) // 2)

    def start_threads(self, locs):
        threads = {}
        for i in range(0, 4):
            threads[i] = threading.Thread(target=blink_block, args=([self.screen, self.FREQ[i], locs[i], self.LSIZE, i + 1]))
            threads[i].setDaemon(True)
            threads[i].start()

    def run_ui(self):
        user_text = ''
        while True:

            for event in pygame.event.get():

                # if user types QUIT then the screen will close
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key in self.ENDSCRN):
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key.unicode in self.DESIRED:
                        self.user_input = event.unicode
                        user_text = ' ' + self.user_input + ' '
                        self.notDesired = False
                    else:
                        self.user_input = ''
                        user_text = ''
                        self.notDesired = True

            # it will set background color of screen
            self.screen.fill(self.BLACK)
            text_surface = self.base_font.render(user_text, True, self.BLACK, self.WHITE)

            # render texts at positions
            self.screen.blit(text_surface, self.text_rect)
            self.screen.blit(self.text_prompt, self.prompt_rect)
            if self.notDesired:
                self.screen.blit(self.text_wrong, self.wrong_rect)

            # update portion of screen
            pygame.display.flip()

            # no more than 60 fps
            self.clock.tick(60)

            size = 100  # size of SSVEP stimuli

            # locations of stimuli blocks (top left corners of each block)
            sub_coord_w = self.X - (30.0 + size)
            sub_coord_h = self.Y - (30.0 + size)
            loc1 = (30.0, 30.0)
            loc2 = (sub_coord_w, 30.0)
            loc3 = (30.0, sub_coord_h)
            loc4 = (sub_coord_w, sub_coord_h)
            locations = (loc1, loc2, loc3, loc4)
            #####

            if not self.threadsOn:
                self.threadsOn = True
                self.start_threads(locations)


if __name__ == "__main__":
    protoUI = UI()
    protoUI.run_ui()
