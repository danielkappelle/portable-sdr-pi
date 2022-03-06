from sdr_pi_config import *
from sdr_pi_display import *
from sdr_pi_input import *
from time import sleep
import signal
import sys

class SdrPiCore:
  def __init__(self):
    self.config = SdrPiConfig()
    self.display = SdrPiDisplay()
    self.input = SdrPiInput()
    self.input.register_knob_0((14,15), self.callback_knob_0)
    self.input.register_btn_0(18, self.callback_btn_0)
    self.received_sigint = False

    signal.signal(signal.SIGINT, self.sigint_handler)

  def callback_knob_0(self, dir):
    if self.config.editing == 'mode':
      self.config.change_mode(dir)
    else:
      self.config.get_mode().update_knob_0(dir)

  def callback_btn_0(self, _):
    self.config.toggle_editing()

  def loop(self):
    while True:
      self.display.update_display(self.config)
      
      if self.received_sigint:
        self.cleanup()
      
      # No delay needed, updating the display is rather slow

  def sigint_handler(self, *_):
    print("Exiting, just a moment")
    self.received_sigint = True

  def cleanup(self):
    self.display.poweroff()
    sys.exit(0)

core = SdrPiCore()
core.loop()