import pygame
import sys
import random
import spidev
import time


class CraneController:

    def __init__(self):
        """
        Crane Controller responsible with controller inputs and sending modification of movements via SPI
        
        Possible Movements are:

        UP: 1
        DOWN: 2
        LEFT: 10
        RIGHT: 20
        HIGH: 100
        LOW: 200

        Possible Movement combinations are:

        UP+LEFT: 11
        UP+RIGHT: 21
        DOWN+LEFT: 12
        DOWN+RIGHT: 22

        UP+HIGH: 101
        UP+LOW: 201
        DOWN+HIGH: 102
        DOWN+LOW: 202
        LEFT+HIGH: 110
        LEFT+LOW: 210
        RIGHT+HIGH: 120
        RIGHT+LOW: 220

        UP+LEFT+HIGH: 111
        UP+LEFT+LOW: 211
        UP+RIGHT+HIGH: 121
        UP+RIGHT+LOW: 221
        DOWN+LEFT+HIGH: 112
        DOWN+LEFT+LOW: 212
        DOWN+RIGHT+HIGH: 122
        DOWN+RIGHT+LOW: 222
        """
        # SPI setup
        self.spi = spidev.SpiDev()
        self.spi.open(1, 0)
        self.spi.max_speed_hz = 90000

        self.move = {
            # Motor 1
            'UP': 0,
            'DOWN': 0,
            # Motor 2
            'LEFT': 0,
            'RIGHT': 0,
            # Motor 3
            'HIGH': 0,
            'LOW': 0
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
        
        # START READING INPUTS FROM USER

        while True:

            for event in pygame.event.get():
                event_d = event.__dict__

                if event.type == pygame.JOYAXISMOTION:  # ARROWS USED

                    if event_d['axis'] == 1:  # ARROWS UP/DOWN PRESSED
                        self.move['UP'] = 1 if event_d['value'] < -1 else 0
                        self.move['DOWN'] = 2 if event_d['value'] == 1 else 0

                    if event_d['axis'] == 0:  # ARROWS LEFT/RIGHT PRESSED
                        self.move['LEFT'] = 10 if event_d['value'] < -1 else 0
                        self.move['RIGHT'] = 20 if event_d['value'] == 1 else 0

                if event.type == pygame.JOYBUTTONDOWN:  # A or B BUTTON PRESSED
                    self.move['HIGH'] = 100 if event_d['button'] == 1 else 0
                    self.move['LOW'] = 200 if event_d['button'] == 0 else 0

                if event.type == pygame.JOYBUTTONUP:  # A or B BUTTON RELEASED
                    self.move['HIGH'] = 0 if event_d['button'] == 1 else 0
                    self.move['LOW'] = 0 if event_d['button'] == 0 else 0

                # For debugging
                # print(self.move)
                self.send_spi()
    
    def send_spi(self):
        """Send SPI command to the Arduino"""
        message = sum([self.move[key] for key in self.move.keys()])

        # For debugging
        # print(message)

        print(self.spi.xfer(message))


if __name__ == '__main__':
    CraneController()
