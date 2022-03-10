# import sys module
import pygame
import sys
import multiprocessing
import threading
from blink import blink_block, generateStimuliSquares

"""Const Init Start"""
# assigning values to X and Y variable
# X = 800
# Y = 600

# color constants
white = (255, 255, 255)
black = (0, 0, 0)

# desired inputs
desired = ('i', 'j', 'k', 'l')
"""Const Init End"""

"""Pygame Init Start"""
# pygame.init() will initialize all
# imported module
pygame.init()
clock = pygame.time.Clock()

# it will display on screen
# screen = pygame.display.set_mode((X, Y))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


X,Y = screen.get_size()


# basic font for user typed
base_font = pygame.font.Font(None, 32)
user_text = ''
"""Pygame Init End"""

# create rectangle
text_rect = pygame.Rect(0, 0, 0, 0)
text_rect.center = (X//2, Y//2 - (base_font.get_height())//2)

# user prompt text
prompt = 'Please enter a command (i/j/k/l):'
text_prompt = base_font.render(prompt, True, white)
prompt_rect = text_prompt.get_rect()
prompt_rect.center = (X//2, Y//2 - (base_font.get_height())*2)

# not desired text
wrong_arg = "Incorrect char inputted"
not_desired = False
text_wrong_arg = base_font.render(wrong_arg, True, white)
wrong_rect = text_wrong_arg.get_rect()
wrong_rect.center = (X//2, (Y//4)*3)

# GUI loop
while True:

    for event in pygame.event.get():

        # if user types QUIT then the screen will close
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.unicode == 'x'):
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # check if key is desired
            for desired_char in desired:
                # if key is desired char, add char to user_text and end loop
                if event.unicode == desired_char:
                    user_input = event.unicode
                    user_text = ' ' + user_input + ' '
                    not_desired = False
                    break
                else:
                    user_text = ''
                    not_desired = True

    # it will set background color of screen
    screen.fill(black)
    text_surface = base_font.render(user_text, True, black, white)

    
    # render texts at positions
    screen.blit(text_surface, text_rect)
    screen.blit(text_prompt, prompt_rect)
    if not_desired:
        screen.blit(text_wrong_arg, wrong_rect)

    # update portion of screen
    pygame.display.flip()

    # no more than 60 fps
    clock.tick(60)

    frequencies = [10, 20, 30, 40] # 10 Hz

    w, h = screen.get_size()
         
    
    size = 200 # size of SSVEP stimuli

    # locations
    subCoordW = w - (30.0 + size)
    subCoordH = h - (30.0 + size)

    loc1 = (30.0, 30.0) # top left (where top corner is (0,0))
    loc2 = (subCoordW, 30.0)
    loc3 = (30.0, subCoordH)
    loc4 = (subCoordW, subCoordH)

    #####


    #### Threads, attempt to use multiprocessing instead....

    thread1 = threading.Thread(target=blink_block, args=([screen, frequencies[0], loc1, size, 1]))
    thread1.setDaemon(True)
    thread1.start()

    thread2 = threading.Thread(target=blink_block, args=([screen, frequencies[1], loc2, size, 2]))
    thread2.setDaemon(True)
    thread2.start()

    thread3 = threading.Thread(target=blink_block, args=([screen, frequencies[2], loc3, size, 3]))
    thread3.setDaemon(True)
    thread3.start()

    thread4 = threading.Thread(target=blink_block, args=([screen, frequencies[3], loc4, size, 4]))
    thread4.setDaemon(True)
    thread4.start()