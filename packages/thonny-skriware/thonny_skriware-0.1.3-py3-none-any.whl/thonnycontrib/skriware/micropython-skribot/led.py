from neopixel import NeoPixel
from machine import Pin


class LED:
  def __init__(self, pin_number):
    self.pin = pin_number
    self.np = NeoPixel(Pin(pin_number, Pin.OUT), 1)
  
  def on(self, r=255, g=255, b=255):
    self.np[0] = r, g, b
    self.np.write()

  def off(self):
    self.np[0] = 0, 0, 0
    self.np.write()
