import pygame
import sys
import random
# import spidev
import time


# spi = spidev.SpiDev()
# spi.open(1, 0)
# spi.max_speed_hz = 90000

# Motor 1
movements = {
    # Motor 1
    'move_up': 0,
    'move_down': 0,
    # Motor 2
    'move_left': 0,
    'move_right': 0,
    # Motor 3
    'move_high': 0,
    'move_low': 0
}

pygame.init()

# Set the width and height of the screen [width,height]
size = [500, 500]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Crane")

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

joystick = pygame.joystick.Joystick(0)
joystick.init()

# -------- Main Program Loop -----------
while True:
    # EVENT PROCESSING STEP
    # User did something
    for event in pygame.event.get():

        event_d = event.__dict__

        if event.type == pygame.JOYAXISMOTION:
            movements['move_up'] = 1 if (
                event_d['axis'] == 1 and event_d['value'] < -1) else 0
            movements['move_down'] = 1 if (
                event_d['axis'] == 1 and event_d['value'] == 1) else 0
            movements['move_left'] = 1 if (
                event_d['axis'] == 0 and event_d['value'] < -1) else 0
            movements['move_right'] = 1 if (
                event_d['axis'] == 0 and event_d['value'] == 1) else 0
        
        if event.type == pygame.JOYBUTTONDOWN:
            movements['move_high'] = 1 if event_d['button'] == 1 else 0
            movements['move_low'] = 1 if event_d['button'] == 0 else 0

        if event.type == pygame.JOYBUTTONUP:
            movements['move_high'] = 0 if event_d['button'] == 1 else 0
            movements['move_low'] = 0 if event_d['button'] == 0 else 0

        print(movements)


# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
