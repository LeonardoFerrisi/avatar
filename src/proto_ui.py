# import sys module
import pygame
import sys

"""Const Init Start"""
# assigning values to X and Y variable
X = 600
Y = 200

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
screen = pygame.display.set_mode((X, Y))

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

while True:
    for event in pygame.event.get():

        # if user types QUIT then the screen will close
        if event.type == pygame.QUIT:
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