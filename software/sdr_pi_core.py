from sdr_pi_config import *
from sdr_pi_display import *
from sdr_pi_input import *
from time import sleep

class SdrPiCore:
  def __init__(self):
    self.config = SdrPiConfig()
    self.display = SdrPiDisplay()
    self.input = SdrPiInput()
    self.input.register_knob_0((14,15), self.callback_knob_0)

  def callback_knob_0(self, dir):
    if self.config.editing == 'mode':
      self.config.change_mode(dir)

  def loop(self):
    while True:
      self.display.update_display(self.config)
      print('yes')

core = SdrPiCore()
SdrPiCore.loop()