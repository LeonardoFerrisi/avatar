# import sys module
from re import L
from stat import ST_UID
import pygame
import sys
import multiprocessing
import threading
from blink import blink_block
import time
from math import sin, pi

class STIMULUS:

    def __init__(self, win):
        self.window = win
    
    def _loop(self):
        time.sleep(0.5)
        COUNT = 1
        clock = pygame.time.Clock()
        frameRate = 60
        frequency = 10 # 10 hz
        
        while True:
            time.sleep(0.01)
            clock.tick(frameRate)
            # somehow this controls the frequency
            tmp = sin(2 * pi * frequency * (COUNT / frameRate))
            color = 255 * (tmp > 0)
            # color = 255
            block = pygame.draw.rect(
                self.window, (color, color, color), pygame.Rect(30, 30, 500, 500))
            pygame.display.update(block)
            COUNT += 1

            if COUNT == frameRate:  # counter goes up until it is equal to the frame rate
                COUNT = 0
                print("Time between frame: " + str(
                    clock.get_time()))  # check the time between each frame (144HZ=7ms; 60HZ=16.67ms)

    def start_loop(self):
        # p = multiprocessing.Process(target=self._loop, args=(), daemon=True)
        # p.start()
        # p.join()

        thread1 = threading.Thread(target=self._loop, args=(), daemon=True)
        thread1.setDaemon(True)
        thread1.start()


class GUI:

    def __init__(self, size : tuple):
        self.size = size 
        pygame.init()
        self.window = pygame.display.set_mode(size)
        self.stimulus = STIMULUS(self.window)
        self.running = True

    def start(self):
        pygame.display.update()
        self.stimulus.start_loop()
        # any calls made to the other thread should be read only
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

        pygame.time.wait(10)
        pygame.quit()
        quit()

if __name__ == "__main__":
    g = GUI(size=(800,600))
    g.start()
