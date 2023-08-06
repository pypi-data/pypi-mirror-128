from machine import PWM
from servo import Servo


class Claw:
  def __init__(self, pin1, pin2):
    self.horizontal_servo = Servo(pin1)
    self.vertical_servo = Servo(pin2)
  
  def open(self):
    self.horizontal_servo.set_angle(90)

  def close(self):
    self.horizontal_servo.set_angle(-90)

  def pick_up(self):
    self.vertical_servo.set_angle(0)

  def put_down(self):
    self.vertical_servo.set_angle(-90)
