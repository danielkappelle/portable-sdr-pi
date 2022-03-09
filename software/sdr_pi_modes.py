from sdr_pi_udp import *
import csv
import os
import subprocess

class SdrPiMode(object):
  def __init__(self):
    self.udp = SdrPiUdp()
    pass

  def activate(self):
    # What should be done when this mode is activated?
    pass

  def deactivate(self):
    # What should be done when this mode is deactivated?
    pass

  def update_knob_0(self, n):
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

  def activate(self):
    self.ps_rtl_fm = subprocess.Popen(('rtl_fm', '-M', 'wbfm', '-f', '102.7M'), stdout=subprocess.PIPE)
    self.ps_sox = subprocess.Popen(('play', '-r', '32k', '-t', 'raw', '-e', 's', '-b', '16', '-c', '1', '-V1', '-'), stdin=self.ps_rtl_fm.stdout)

  def deactivate(self):
    self.ps_sox.kill()
    self.ps_rtl_fm.kill()

  def update_knob_0(self, n):
    self.freq += n/10

  def update_stream(self):
    self.udp.set_mode('FM')
    self.udp.set_freq(self.freq*1E6)
    pass

  def get_channel_display(self):
    return "%.1f\nMHz" % self.freq

class ModeCBFM(SdrPiMode):
  def __init__(self):
    super().__init__()
    self.display_name = "CB"
    self.channel = 0
    
    with open(os.path.join(os.path.dirname(__file__), 'assets/cb_channels.csv')) as f:
      reader = csv.reader(f)
      self.channels = {int(rows[0]):float(rows[1]) for rows in reader}
      
  def activate(self):
    self.ps_rtl_fm = subprocess.Popen(('rtl_fm', '-M', 'fm', '-r', '8k', '-f', '%.3fM' % (self.channels[self.channel+1]*1E6)), stdout=subprocess.PIPE)
    self.ps_sox = subprocess.Popen(('play', '-r', '8k', '-t', 'raw', '-e', 's', '-b', '16', '-c', '1', '-V1', '-'), stdin=self.ps_rtl_fm.stdout)

  def deactivate(self):
    self.ps_sox.kill()
    self.ps_rtl_fm.kill()

  def update_knob_0(self, n):
    self.channel = (self.channel + n) % len(self.channels)

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
      reader = csv.reader(f)
      self.channels = [[float(row[0]), row[1].replace('\\n','\n')] for row in reader]
    
  def activate(self):
    self.ps_rtl_fm = subprocess.Popen(('rtl_fm', '-M', 'am', '-r', '8k', '-f', '%.3fM' % (self.channels[self.channel][0]*1E6)), stdout=subprocess.PIPE)
    self.ps_sox = subprocess.Popen(('play', '-r', '8k', '-t', 'raw', '-e', 's', '-b', '16', '-c', '1', '-V1', '-'), stdin=self.ps_rtl_fm.stdout)

  def deactivate(self):
    self.ps_sox.kill()
    self.ps_rtl_fm.kill()

  def update_knob_0(self, n):
    self.channel = (self.channel + n) % len(self.channels)

  def update_stream(self):
    self.udp.set_mode('AM')
    self.udp.set_freq(self.channels[self.channel][0]*1E6)

  def get_channel_display(self):
    return self.channels[self.channel][1] + ("\n%.3f" % self.channels[self.channel][0])
