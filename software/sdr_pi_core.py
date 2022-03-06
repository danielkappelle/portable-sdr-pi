from sdr_pi_config import *
from sdr_pi_display import *
from sdr_pi_input import *
from time import sleep
import signal
import sys
import subprocess

class SdrPiCore:
  def __init__(self):
    self.config = SdrPiConfig()
    self.display = SdrPiDisplay()
    self.input = SdrPiInput()
    self.input.register_knob_0((14,15), self.callback_knob_0)
    self.input.register_btn_0(18, self.callback_btn_0)
    self.received_sigint = False
    self.pristine = True

    # Start the stream
    self.ps_rtl_fm = subprocess.Popen(('rtl_fm', '-M', 'wbfm', '-f', '102.7M'), stdout=subprocess.PIPE)
    self.ps_sox = subprocess.Popen(('play', '-r', '32k', '-t', 'raw', '-e', 's', '-b', '16', '-c', '1', '-V1', '-'), stdin=self.ps_rtl_fm.stdout)

    signal.signal(signal.SIGINT, self.sigint_handler)

  def callback_knob_0(self, dir):
    if self.config.editing == 'mode':
      self.config.change_mode(dir)
    else:
      self.config.get_mode().update_knob_0(dir)

    self.pristine = False

  def callback_btn_0(self, _):
    self.config.toggle_editing()

  def loop(self):
    while True:
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
    self.ps_sox.kill()
    self.ps_rtl_fm.kill()
    self.display.poweroff()
    sys.exit(0)

core = SdrPiCore()
core.loop()