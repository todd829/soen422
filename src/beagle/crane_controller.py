from pynput import keyboard
import sys
import random
import spidev
import time
        

class CraneController:

    def __init__(self):
        """Crane Controller responsible with key change and sending modification of movements via SPI"""
        # spi setup
        self.spi = spidev.SpiDev()
        self.spi.open(1, 0)
        self.spi.max_speed_hz = 90000

        # Motor 1
        self.movements = {
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

        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def on_press(self, key):
        """On Press of a certain key, modify movements and send vie SPI"""

        move_by_key_press = {
            keyboard.KeyCode.from_char('w'): self.movements['move_up'],
            keyboard.KeyCode.from_char('a'): self.movements['move_left'],
            keyboard.KeyCode.from_char('s'): self.movements['move_down'],
            keyboard.KeyCode.from_char('d'): self.movements['move_right'],
            keyboard.KeyCode.from_char('r'): self.movements['move_high'],
            keyboard.KeyCode.from_char('f'): self.movements['move_low']
        }

        if key in move_by_key_press.keys():
            if move_by_key_press[key] == 0:
                move_by_key_press[key] = 1
                self.send_spi_command()

    def on_release(self, key):
        """On Release of a certain key, modify movements and send vie SPI"""

        if key == keyboard.Key.esc:
            self.end()

        move_by_key_release = {
            keyboard.KeyCode.from_char('w'): self.movements['move_up'],
            keyboard.KeyCode.from_char('a'): self.movements['move_left'],
            keyboard.KeyCode.from_char('s'): self.movements['move_down'],
            keyboard.KeyCode.from_char('d'): self.movements['move_right'],
            keyboard.KeyCode.from_char('r'): self.movements['move_high'],
            keyboard.KeyCode.from_char('f'): self.movements['move_low']
        }

        if key in move_by_key_release.keys():
            if move_by_key_release[key] == 1:
                move_by_key_release[key] = 0
                self.send_spi_command()
    
    def spi_command(self):
        """Create SPI command to send in the form [0, 0, 0, 0, 0, 0] where each group of 2 are a motor's drive/reverse"""
        return [
            self.movements['move_up'], self.movements['move_down'],
            self.movements['move_left'], self.movements['move_right'],
            self.movements['move_high'], self.movements['move_low']
            ]

    def send_spi_command(self):
        """Send SPI command to the Arduino"""
        command = self.spi_command()
        print(self.spi.xfer(command))
        time.sleep(1)
        
    def end(self):
        """End the app on ESC"""
        sys.exit(1)


if __name__ == '__main__':
    CraneController()
