from sdr_pi_modes import *

class SdrPiConfig:
  def __init__(self):
    self.modes = [
      ModeFM(),
      ModeCB(),
      ModeAirbandPresets()
    ]

    self.current_mode = 0
    self.editing = 'mode'

  def get_mode(self):
    return self.modes[self.current_mode]

  def change_mode(self, dir):
    self.current_mode = (self.current_mode + dir) % len(self.modes)

  def toggle_editing(self):
    if self.editing == 'mode':
      self.editing = 'channel'
    else:
      self.editing = 'mode'
    
