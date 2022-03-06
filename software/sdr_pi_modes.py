from sdr_pi_udp import *

class SdrPiMode(object):
  def __init__(self):
    self.display_name = ""
    self.udp = SdrPiUdp()
    pass

  def update_knob_0(self, dir):
    # What should happen in this mode if the first knob has changed
    pass

  def update_stream(self):
    # What should be done when the audio stream needs to be updated
    pass

  def get_channel_display(self):
    # What should be displayed as channel/freq
    pass

class ModeFM(SdrPiMode):
  def __init__(self):
    self.display_name = "FM"
    self.freq = 102.7 # In MHz
    super().__init__()

  def update_knob_0(self, dir):
    self.freq += dir/10

  def update_stream(self):
    self.udp.set_mode('FM')
    self.udp.set_freq(self.channels[self.channel+1]*1E6)
    pass

  def get_channel_display(self):
    return "%.1f\nMHz" % self.freq

class ModeCB(SdrPiMode):
  def __init__(self):
    self.display_name = "Preset\nCB"
    self.channel = 0
    self.channels = {
      1: 26.965,
      2: 26.975,
      3: 26.985,
      4: 27.005,
      5: 27.015
    }
    super().__init__()

  def update_knob_0(self, dir):
    self.channel = (self.channel + dir) % len(self.channels)

  def update_stream(self):
    self.udp.set_mode('FM')
    self.udp.set_freq(self.channels[self.channel+1]*1E6)

  def get_channel_display(self):
    return "%d" % (self.channel+1)