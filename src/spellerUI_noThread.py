# import sys module
from operator import pos
from turtle import back
import pygame
import sys
import numpy as np
from blink import blink_block, generateStimuliSquares
import time
import math

def draw_stimuli(j,win, positions, frequencies, size):
    i=0
    for frequency in frequencies:
        result = math.sin(2 * math.pi * frequency * j / 60)
        sign = lambda x: (1, 0)[x < 0]
        color = 255 * sign(result)
        colors = [color, color, color]
        pose = positions[i]
        getRekt =  pygame.Rect(pose[0], pose[1], size, size)
        pygame.draw.rect(win, colors, getRekt)
        pygame.display.update()
        i+=1

    """
    _summary_: Updates the letters on the screen
    @param win: The pygame.Surface obj (screen)
    @param letters: List of lists of letters
    @param levelsIn: How many levels in the lists are we?
    """
def update_letters(screen, letters : list, levelsIn : int, positions, stimSize : int):
    # positions for boxes
    x1, y1 = positions[0]
    x2, y2 = positions[1]
    x3, y3 = positions[2]
    x4, y4 = positions[3]
    
    # render and prompt text
    box1 = str(letters[0])
    box2 = str(letters[1])
    box3 = str(letters[2])
    box4 = str(letters[3])
    # boxes = [box1, box2, box3, box4]
    # v = 0
    # for set in letters:
    #     for char in set:
    #         toAdd = " "+char+" "
    #         boxes[v]+=toAdd
    #     v+=1
    
    #box1
    
    distFrom = 200
    box1_txt = base_font.render(box1, True, green, black)
    box1_rect = box1_txt.get_rect()
    box1_rect.center = (x1+stimSize+distFrom, y1+40)
    box2_txt = base_font.render(box2, True, green, black)
    box2_rect = box2_txt.get_rect()
    box2_rect.center = (x2-distFrom, y2+40)
    box3_txt = base_font.render(box3, True, green, black)
    box3_rect = box3_txt.get_rect()
    box3_rect.center = (x3+stimSize+distFrom, y3+40)
    box4_txt = base_font.render(box4, True, green, black)
    box4_rect = box4_txt.get_rect()
    box4_rect.center = (x4-distFrom, y4+40)
    
    screen.blit(box1_txt, (box1_rect.left, box1_rect.top))
    screen.blit(box2_txt, (box2_rect.left, box2_rect.top))
    screen.blit(box3_txt, (box3_rect.left, box3_rect.top))
    screen.blit(box4_txt, (box4_rect.left, box4_rect.top))
    
    #####
    
    txtBoxSize = (350, 100)
    
    # box 1: 
    x1+=stimSize
    txtRect = pygame.Rect(x1+20, y1, txtBoxSize[0], txtBoxSize[1])
    pygame.draw.rect(screen, blue, txtRect, 3)  # width = 3
    
    # box 2: 
    x2-=stimSize
    txtRect = pygame.Rect(x2-220, y2, txtBoxSize[0], txtBoxSize[1])
    pygame.draw.rect(screen, blue, txtRect, 3)  # width = 3
    
    # box 3: 
    x3+=stimSize
    txtRect = pygame.Rect(x3+20, y3, txtBoxSize[0], txtBoxSize[1])
    pygame.draw.rect(screen, blue, txtRect, 3)  # width = 3
    
    # box 4: 
    x4-=stimSize
    txtRect = pygame.Rect(x4-220, y4, txtBoxSize[0], txtBoxSize[1])
    pygame.draw.rect(screen, blue, txtRect, 3)  # width = 3

if __name__ == "__main__":
    """Const Init Start"""
    # assigning values to X and Y variable
    # X = 800
    # Y = 600
    threadsOn = False
    # color constants
    white = (255, 255, 255)
    black = (0, 0, 0)
    green = (0, 255, 0)
    blue = (0, 100, 255)

    # desired inputs
    desired = ('i', 'j', 'k', 'l')
    """Const Init End"""

    """Pygame Init Start"""
    # pygame.init() will initialize all
    # imported module
    pygame.init()
    # clock = pygame.time.Clock()


    current_time = pygame.time.get_ticks()
    # time of next change
    delay = 1000. / 60 # Rn delay is 16.666 where Screen rate is 60 Hz
    change_time = current_time + delay
    show = True
    j=0

    # it will display on screen
    # screen = pygame.display.set_mode((X, Y))
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


    X,Y = screen.get_size()

    print("DIMENSIONS: "+str(X)+", "+str(Y))

    # basic font for user typed
    base_font = pygame.font.Font(None, 32)
    user_text = ''
    """Pygame Init End"""

    # create rectangle
    text_rect = pygame.Rect(0, 0, 0, 0)
    text_rect.center = (X//2, Y//2 - (base_font.get_height())//2)

    #bckgrnd rectangle 
    bk_rect = pygame.Rect(0, 0, 400, Y)
    bk_rect.center = (X//2, Y//2 - (base_font.get_height())//2)
    
    # user prompt text
    prompt = 'Please enter a command (i/j/k/l):'
    text_prompt = base_font.render(prompt, True, green, black)
    prompt_rect = text_prompt.get_rect()
    prompt_rect.center = (X//2, Y//2 - (base_font.get_height())*2)

    # not desired text
    wrong_arg = "Incorrect char inputted"
    not_desired = False
    text_wrong_arg = base_font.render(wrong_arg, True, green, black)
    wrong_rect = text_wrong_arg.get_rect()
    wrong_rect.center = (X//2, (Y//4)*3)
    
    # stimuli locations #######################################
    w, h = screen.get_size()    
    size = 150 # size of SSVEP stimuli
    # locations
    subCoordW = w - (30.0 + size)
    subCoordH = h - (30.0 + size)
    loc1 = (30.0, 30.0) # top left (where top corner is (0,0))
    loc2 = (subCoordW, 30.0)
    loc3 = (30.0, subCoordH)
    loc4 = (subCoordW, subCoordH)
    locations = [loc1, loc2, loc3, loc4]
    ###########################################################
    
    # Text lists for boxes (start as intial are updated by ui)
    tl = ["A", "E", "I", "O", "T", "N", "R", "S"]
    tr = ["O", "C", "U", "D", "P", "M", "H", "G"]
    bl = ["B", "F", "Y", "W", "K", "V", "X", "Z"]
    br = ["J", "Q", "?", "!", ",", ":)", ":(", "O_O"]
    
    currentChars = [tl, tr, bl, br]
    lvlIn = 0
    
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
        # screen.fill(black)
        

        text_surface = base_font.render(user_text, True, green, black)

        
        # render texts at positions
        pygame.draw.rect(screen, black, bk_rect)
        
        update_letters(screen=screen, letters=currentChars, levelsIn=lvlIn, positions=locations, stimSize=size)
        
        # screen.blit()
        screen.blit(text_surface, text_rect)
        screen.blit(text_prompt, prompt_rect)
        if not_desired:
            screen.blit(text_wrong_arg, wrong_rect)

        # update portion of screen
        pygame.display.flip()


        # no more than 60 fps
        # clock.tick(60)

        
        frequencies = [6.67, 7.5 ,8.57, 10] # 10 Hz

        

        



        current_time = pygame.time.get_ticks()

        # is time to change ?
        if current_time >= change_time:
            # time of next change
            
            change_time = current_time + delay 
            show = not show
            draw_stimuli(j, win=screen, positions=locations, frequencies=frequencies, size=size)
            pygame.display.update()
            j+=1