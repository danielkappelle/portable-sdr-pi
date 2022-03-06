from sdr_pi_config import *
from sdr_pi_display import *
from sdr_pi_input import *
from time import sleep

def callback_knob_0(dir):
  print("Dir: %d" % dir)

config = SdrPiConfig()
display = SdrPiDisplay()
input = SdrPiInput()
input.register_knob_0((14,15), callback_knob_0)

while True:
  display.update_display(config)
  sleep(1)