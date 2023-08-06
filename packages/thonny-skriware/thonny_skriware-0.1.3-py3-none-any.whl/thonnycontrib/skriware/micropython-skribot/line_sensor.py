from machine import Pin, ADC


class LineSensor:
  def __init__(self, pin_number, threshold=2048):
    self.pin = pin_number
    self.adc = ADC(Pin(self.pin, Pin.IN))
    self.threshold = threshold
  
  def read(self):
    return self.read_raw() < self.threshold
  
  def read_raw(self):
    return self.adc.read()
