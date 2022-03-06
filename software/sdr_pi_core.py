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
    self.input.register_btn_0(18, self.callback_btn_0)

  def callback_knob_0(self, dir):
    if self.config.editing == 'mode':
      self.config.change_mode(dir)
    else:
      self.config.get_mode().update_knob_0(dir)

  def callback_btn_0(self):
    self.config.toggle_editing()

  def loop(self):
    while True:
      self.display.update_display(self.config)
      # No delay needed, updating the display is rather slow

core = SdrPiCore()
core.loop()