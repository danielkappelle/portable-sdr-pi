import socket
import os

DEBUG = "DEBUG" in os.environ

class SdrPiUdp:
  def __init__(self):
    self.connect()
    pass

  def connect(self):
    self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.s.connect(("localhost", 6020))

  def set_freq(self, freq):
    freq = int(freq)
    buf = (0).to_bytes(1, 'little') + freq.to_bytes(4, 'little')

    try:
      self.s.send(buf)
    except socket.error:
      try:
        self.connect()
        self.s.send(buf)
      except socket.error:
        print("ERROR: can't connect to UDP")

  def set_mode(self, mode):
    modes = {
      'FM': 0,
      'AM': 1,
      'USB': 2,
      'LSB': 3
    }

    buf = (1).to_bytes(1, 'little') + modes[mode].to_bytes(4, 'little')
