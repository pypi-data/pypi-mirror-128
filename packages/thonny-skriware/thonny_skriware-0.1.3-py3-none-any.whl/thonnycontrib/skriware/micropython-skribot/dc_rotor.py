from machine import Pin, PWM


class DCRotor:
  def __init__(self, pin1, pin2):
    self.pwm1 = PWM(Pin(pin1), freq=2000)
    self.pwm2 = PWM(Pin(pin2), freq=2000)
    self.stop()

  def move_forward(self, speed=1.0):
    self.pwm1.duty(int(speed * 1023))
    self.pwm2.duty(0)

  def move_backward(self, speed=1.0):
    self.pwm1.duty(0)
    self.pwm2.duty(int(speed * 1023))
  
  def stop(self):
    self.pwm1.duty(0)
    self.pwm2.duty(0)
  
  def hard_stop(self):
    self.pwm1.duty(1023)
    self.pwm2.duty(1023)
