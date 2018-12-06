import random
import spidev
import time
spi = spidev.SpiDev()
spi.open(1, 0)
spi.max_speed_hz = 90000

while(True):
        to_send = [random.randrange(1,250,25)]
        print spi.xfer(to_send) 
        time.sleep(1)
