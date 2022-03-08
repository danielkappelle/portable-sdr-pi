
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageFont, ImageDraw
import os

class SdrPiDisplay:
  def __init__(self, display_width = 128, display_height = 64, addr = 0x3c):
    self.display_width = display_width
    self.display_height = display_height
    self.addr = addr
    
    # Set up I2C
    self.i2c = busio.I2C(board.SCL, board.SDA)

    # Set up oled screen
    self.oled = adafruit_ssd1306.SSD1306_I2C(self.display_width, self.display_height, self.i2c, addr=self.addr)

    # Maybe do a splash screen later?
    self.oled.fill(0)
    self.oled.show()

    # Set up the image we'll be working with
    self.image = Image.new("1", (self.oled.width, self.oled.height))
    self.draw = ImageDraw.Draw(self.image)
    self.font = ImageFont.truetype(os.path.join(os.path.dirname(__file__),"assets/arial.ttf"), 12)
    self.channel_font_size = 12
    self.channel_font = ImageFont.truetype(os.path.join(os.path.dirname(__file__),"assets/arial.ttf"), self.channel_font_size)

  def update_display(self, config):
    # First update the mode
    mode = config.get_mode().display_name
    (font_width, font_height) = self.font.getsize(mode)
    self.draw.rectangle((0, 0, self.display_width//2, self.display_height), fill=0) # Erase area
    self.draw.text((6, self.display_height//2-font_height//2), mode, font=self.font, fill=255)

    # Update channel/frequency
    channel = config.get_mode().get_channel_display()
    self.channel_font_size = 12
    while self.channel_font.getsize(channel)[0] > (self.display_width/2-4) and self.channel_font_size >= 10:
      self.channel_font_size -= 1
      self.channel_font = ImageFont.truetype(os.path.join(os.path.dirname(__file__),"assets/arial.ttf"), self.channel_font_size)
    
    (font_width, font_height) = self.channel_font.getsize(channel)
    self.draw.rectangle((self.display_width//2, 0, self.display_width, self.display_height), fill=0)
    self.draw.text((70, self.display_height//2-font_height//2), channel, font=self.channel_font, fill=255)

    # Update changing box
    if config.editing == "channel":
      self.draw.rectangle((self.display_width//2+4, 4, self.display_width-4, self.display_height-4), fill=None, outline=255)
      self.draw.rectangle((4, 4, self.display_width//2-4, self.display_height-4), fill=None, outline=0)
    else:
      self.draw.rectangle((self.display_width//2+4, 4, self.display_width-4, self.display_height-4), fill=None, outline=0)
      self.draw.rectangle((4, 4, self.display_width//2-4, self.display_height-4), fill=None, outline=255)

    self.oled.image(self.image)
    self.oled.show()

  def poweroff(self):
    self.oled.poweroff()
