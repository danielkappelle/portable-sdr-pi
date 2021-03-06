from sdr_pi_config import *
from sdr_pi_display import *
from sdr_pi_input import *
from time import sleep
import signal
import sys
import subprocess
import os

class SdrPiCore:
  def __init__(self):
    self.config = SdrPiConfig()
    self.display = SdrPiDisplay()
    self.input = SdrPiInput()
    self.input.register_knob_0((14,15), self.callback_knob_0)
    self.input.register_btn_0(18, self.callback_btn_0)
    self.received_sigint = False
    self.pristine = True
    self.knob_changed = 0

    signal.signal(signal.SIGINT, self.sigint_handler)

  def callback_knob_0(self, dir):
    self.knob_changed += dir

  def callback_btn_0(self, _):
    self.config.toggle_editing()

  def loop(self):
    while True:
      if self.knob_changed != 0:
        if self.config.editing == 'mode':
          self.config.change_mode(1 if self.knob_changed > 0 else -1)
        else:
          self.config.get_mode().update_knob_0(self.knob_changed)
          self.pristine = False
        self.knob_changed = 0
      self.display.update_display(self.config)
      
      if not self.pristine:
        self.config.get_mode().update_stream()
        self.pristine = True
      
      if self.received_sigint:
        self.cleanup()
      
      # No delay needed, updating the display is rather slow

  def sigint_handler(self, *_):
    print("Exiting, just a moment")
    self.received_sigint = True

  def cleanup(self):
    self.config.get_mode().deactivate()
    self.display.poweroff()
    sys.exit(0)

DEBUG = "DEBUG" in os.environ

core = SdrPiCore()
core.loop()
