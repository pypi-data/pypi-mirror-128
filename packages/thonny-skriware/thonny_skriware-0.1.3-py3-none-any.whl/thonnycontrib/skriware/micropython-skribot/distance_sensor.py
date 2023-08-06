import time

from machine import Pin, time_pulse_us


class DistanceSensor:
  def __init__(self, trig, echo):
    self.pins = trig, echo
    self.trig = Pin(trig, Pin.OUT)
    self.echo = Pin(echo, Pin.IN)

    self.trig.off()
  
  def read_raw(self):
    self.trig.off()
    time.sleep_us(5)
    self.trig.on()
    time.sleep_us(10)
    self.trig.off()

    timeout = 30000
    pulse_time = time_pulse_us(self.echo, 1, timeout)
    return pulse_time
  
  def read(self):
    return self.read_raw() / 58
    