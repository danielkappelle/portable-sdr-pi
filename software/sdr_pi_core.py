from sdr_pi_config import *
from sdr_pi_display import *
from time import sleep

config = SdrPiConfig()
display = SdrPiDisplay()

while True:
  display.update_display(config)
  sleep(1)