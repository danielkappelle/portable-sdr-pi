import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageFont, ImageDraw
from encoder.encoder import Encoder
import RPi.GPIO as GPIO
import time
import os
import socket


freq = 102.7
mods = ['wbfm', 'am']
mod = 0
changing = 'freq'

def enc_changed(val, dir):
    global freq, mod, mods
    if dir == 'L':
        dir = -1
    else:
        dir = 1

    if changing == 'freq':
        freq = freq + dir/10
    else:
        mod = (mod + dir) % len(mods)

def button_pressed(channel):
    global changing
    if changing == 'freq':
        changing = 'mod'
        update_sdr()
    else:
        changing = 'freq'

def update_sdr():
    global s
    print("Tune station")
    buf = (0).to_bytes(1, 'little') + int(freq*1E6).to_bytes(4, 'little')
    s.send(buf)

i2c = busio.I2C(board.SCL, board.SDA)
GPIO.setmode(GPIO.BCM)
enc = Encoder(14,15, callback=enc_changed)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(18, GPIO.FALLING, callback=button_pressed, bouncetime=300)

WIDTH = 128
HEIGHT = 64

oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3c)

oled.fill(0)
oled.show()

image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
font = ImageFont.truetype(os.path.join(os.path.dirname(__file__),"Arial.ttf"), 12)

def update_freq():
    text = "%.3f\n MHz" % freq
    (font_width, font_height) = font.getsize(text)
    draw.rectangle((WIDTH//2, 0, WIDTH, HEIGHT), fill=0)
    draw.text((70, HEIGHT//2-font_height//2), text, font=font, fill=255)

def update_mod():
    (font_width, font_height) = font.getsize(mods[mod])
    draw.rectangle((0, 0, WIDTH//2, HEIGHT), fill=0)
    draw.text((6, HEIGHT//2-font_height//2), mods[mod], font=font, fill=255)

def update_changing():
    if changing == 'freq':
        draw.rectangle((WIDTH//2+4, 4, WIDTH-4, HEIGHT-4), fill=None, outline=255)
        draw.rectangle((4, 4, WIDTH//2-4, HEIGHT-4), fill=None, outline=0)
    else:
        draw.rectangle((WIDTH//2+4, 4, WIDTH-4, HEIGHT-4), fill=None, outline=0)
        draw.rectangle((4, 4, WIDTH//2-4, HEIGHT-4), fill=None, outline=255)


def draw_now():
    oled.image(image)
    oled.show()

update_freq()
update_mod()
draw_now()

os.system("rtl_fm -M %s -f %.3fM | play -r 32k -t raw -e s -b 16 -c 1 -V1 - &" % (mods[mod], freq) )

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("localhost", 6020))

while True:
    update_freq()
    update_mod()
    update_changing()
    draw_now()
    
