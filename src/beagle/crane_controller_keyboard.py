import keyboard
import sys
import random
# import spidev
import time
        

class CraneController:

    def __init__(self):
        """
        Crane Controller responsible with key change and sending modification of movements via SPI
        
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
        # spi setup
        # self.spi = spidev.SpiDev()
        # self.spi.open(1, 0)
        # self.spi.max_speed_hz = 90000

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

        keyboard.on_press(self.on_press)
        keyboard.on_release(self.on_release)

        # Wait on ESC to exit
        keyboard.wait('esc')

    def on_press(self, key_obj):
        """On Press of a certain key, modify movements and send vie SPI"""
        key = key_obj.__dict__['name']
        print(key, key_obj.__dict__)

        by_key_press = {
            'w': [self.move['UP'], 1],
            'a': [self.move['DOWN'], 2],
            's': [self.move['LEFT'], 10],
            'd': [self.move['RIGHT'], 20],
            'r': [self.move['HIGH'], 100],
            'f': [self.move['LOW'], 200]
        }

        if key in by_key_press.keys():
            if by_key_press[key][0] == 0:
                by_key_press[key][0] = by_key_press[key][1]
                self.send_spi()

    def on_release(self, key_obj):
        """On Release of a certain key, modify movements and send vie SPI"""

        key = key_obj.__dict__['name']
        print(key, key_obj.__dict__)

        by_key_release = {
            'w': (self.move['UP'], 1),
            'a': (self.move['DOWN'], 2),
            's': (self.move['LEFT'], 10),
            'd': (self.move['RIGHT'], 20),
            'r': (self.move['HIGH'], 100),
            'f': (self.move['LOW'], 200)
        }

        if key in by_key_release.keys():
            if by_key_release[key][0] == by_key_release[key][1]:
                by_key_release[key][0] = 0
                self.send_spi()

    def send_spi(self):
        """Send SPI command to the Arduino"""
        message = sum([self.move[key] for key in self.move.keys()])

        # For debugging
        print(message)

        #print(self.spi.xfer(message))
        
    def end(self):
        """End the app on ESC"""
        sys.exit(1)


if __name__ == '__main__':
    CraneController()