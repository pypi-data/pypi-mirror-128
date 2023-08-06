from machine import Pin, PWM


class Servo:
  def __init__(self, pin):
    self.pwm = PWM(Pin(pin), freq=50) 
    self.pwm.duty(int(1023 * 0.05))
  
  def set_angle(self, a_):
    '''a = angle in deg. from -90 to 90'''

    a = sorted((-90, a_, 90))[1]

    a += 90 # range 0-180
    a /= 3600 # range 0-0.05
    duty = int(1023 * (a + 0.05))
    self.pwm.duty(duty)
