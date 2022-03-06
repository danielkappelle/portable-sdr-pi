from encoder.encoder import Encoder
import RPi.GPIO as GPIO

class SdrPiInput:
  def __init__(self):
    GPIO.setmode(GPIO.BCM)
    
  def register_knob_0(self, pins, callback):
    # Initalize encoder

    def callback_wrapper(value, dir):
      if dir == "L":
        dir = -1
      else:
        dir = 1
      callback(dir)
    
    self.enc = Encoder(pins[0], pins[1], callback=callback_wrapper)

  def register_btn_0(self, pin, callback):
    GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(pin, GPIO.FALLING, callback=callback, bouncetime=300)