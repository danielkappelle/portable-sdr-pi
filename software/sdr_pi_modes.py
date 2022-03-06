class SdrPiMode:
  def __init__(self):
    self.display_name = ""
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

  def update_knob_0(self, dir):
    self.freq += dir/10

  def update_stream(self):
    # Invoke UDP command here
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

  def update_knob_0(self, dir):
    self.channel = (self.channel + dir) % len(self.channels)

  def update_stream(self):
    # Invoke UDP command
    pass

  def get_channel_display(self):
    return "%d" % (self.channel+1)