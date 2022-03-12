import pygame
from math import sin, pi
import time


def blink_block(win, frequency, location: tuple, size : int, blockNum : int):
    COUNT = 1
    clock = pygame.time.Clock()
    startTime = time.time()

    # frameRate = 200

    # if frequency==10:
    #     frameRate = 200
    # elif frequency==14 or frequency == 12:
    #     frameRate = 120
    # elif frequency==16:
    #     frameRate = 80
    # elif frequency == 20:
    #     frameRate = 60
    frameRate = 60
    # b.wait()

    while True:
        clock.tick(frameRate)
        # somehow this controls the frequency
        tmp = sin(2 * pi * frequency * (COUNT / frameRate))
        color = 255 * (tmp > 0)
        # color = 255

        # print(str(color))

        block = pygame.draw.rect(
            win, (color, color, color), pygame.Rect(location[0], location[1], size, size))
        pygame.display.update(block)
        COUNT += 1

        # if COUNT == frameRate:  # counter goes up until it is equal to the frame rate
        #     COUNT = 0
        #     print("Time between frame: " + str(
        #     clock.get_time()))  # check the time between each frame (144HZ=7ms; 60HZ=16.67ms)
        timeElapsed = (time.time() - startTime)*1000.0
        # print(f"TimeElapsed: {timeElapsed}")
        if (timeElapsed > 1000.0):
            freq = 1000.0//COUNT
            COUNT = 0
            print(f"Frequency of block #{blockNum} :{freq}")
            startTime = time.time()


def generateStimuliSquares(screen, side_len: int):
    '''
    Generates the 4 squares
    @param win: the pygame display obj
    @return: A list containing squares in the order, topL, topR, botL, botR
    '''
    squares = []

    w, h = screen.get_size()  # get the dimensions of thw window

    subCoordW = w - (30.0 + side_len)  # for items on the other side
    subCoordH = h - (30.0 + side_len)  # for items on the other side

    topLeft = pygame.Rect(30.0, 30.0, side_len, side_len)

    topRight = pygame.Rect(subCoordW, 30.0, side_len, side_len)

    bottomLeft = pygame.Rect(30.0, subCoordH, side_len, side_len)

    bottomRight = pygame.Rect(subCoordW, subCoordH, side_len, side_len)

    squaresToReturn = [topLeft, topRight, bottomLeft, bottomRight]

    return 