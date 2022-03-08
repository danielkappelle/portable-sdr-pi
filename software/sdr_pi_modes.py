from sdr_pi_udp import *
import csv
import os

class SdrPiMode(object):
  def __init__(self):
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
    super().__init__()
    self.display_name = "FM"
    self.freq = 102.7 # In MHz

  def update_knob_0(self, dir):
    self.freq += dir/10

  def update_stream(self):
    self.udp.set_mode('FM')
    self.udp.set_freq(self.freq*1E6)
    pass

  def get_channel_display(self):
    return "%.1f\nMHz" % self.freq

class ModeCB(SdrPiMode):
  def __init__(self):
    super().__init__()
    self.display_name = "CB"
    self.channel = 0
    
    with open(os.path.join(os.path.dirname(__file__), 'assets/cb_channels.csv')) as f:
      reader = csv.reader(f)
      self.channels = {int(rows[0]):float(rows[1]) for rows in reader}
      

  def update_knob_0(self, dir):
    self.channel = (self.channel + dir) % len(self.channels)

  def update_stream(self):
    self.udp.set_mode('FM')
    self.udp.set_freq(self.channels[self.channel+1]*1E6)

  def get_channel_display(self):
    return "%d" % (self.channel+1)

class ModeAirbandPresets(SdrPiMode):
  def __init__(self):
    super().__init__()
    self.display_name = "Airband\npresets"
    self.channel = 0

    with open(os.path.join(os.path.dirname(__file__), 'assets/airband_channel_presets.csv')) as f:
      reader = csv.reader()
      self.channels = [[float(row[0]), row[1]] for row in reader]
    
  def update_knob_0(self, dir):
    self.channel = (self.channel + dir) % len(self.channels)

  def update_stream(self):
    self.udp.set_mode('AM')
    self.udp.set_freq(self.channels[self.channel][0]*1E6)

  def get_channel_display(self):
    return self.channels[self.channel][1] + ("\n%.3f" % self.channels[self.channel][0])