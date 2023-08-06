import time

import skribrain
import skribrain3

from machine import Pin

from claw import Claw
from dc_rotor import DCRotor
from distance_sensor import DistanceSensor
from led import LED
from line_sensor import LineSensor


class Skribot:
  def __init__(self, predef=None):
    self._claws = []
    self._left_dc_rotors = []
    self._right_dc_rotors = []
    self._dist_sensors = []
    self._leds = []
    self._qtrs = []
    self._app_switch = None

    self._speed = 255

    if predef is not None:
      self.configure_connections(predef)

    self.relax()

  @property
  def normspeed(self):
    '''Normalized speed'''
    return self._speed / 255

  @property
  def speed(self):
    return self._speed

  @speed.setter
  def speed(self, val):
    self._speed = sorted((0, val, 255))[1]

  @property
  def _dc_rotors(self):
    return self._left_dc_rotors + self._right_dc_rotors

  @property
  def app_switch(self):
    return self._app_switch

  def configure_connections(self, predef):
    if predef in ('SKRIBRAIN', 'SKRIBRAIN3', 'SKRIBRAIN2'):
      self.add_dc_rotor(skribrain.MOTOR1, 'LEFT')
      self.add_dc_rotor(skribrain.MOTOR3, 'RIGHT')
      self.add_led(skribrain.LED1)
      self.add_led(skribrain.LED2)
      self.add_claw(predef=predef)
      self.add_distance_sensor(skribrain.D1)
      self.add_distance_sensor(skribrain.D2)
      self.add_line_sensor(skribrain.LINE1)
      self.add_line_sensor(skribrain.LINE2)
      self.add_line_sensor(skribrain.LINE3)
      if predef in ('SKRIBRAIN', 'SKRIBRAIN3'):
        self._app_switch = Pin(skribrain3.APP_SWITCH, Pin.IN, pull=Pin.PULL_UP)

  def _delay(self, ms):
    try:
      time.sleep(ms/1000)
    finally:
      self.Stop()

  def stress(self):
    self.pick_up()
    self.close_claw()
    self.move_slowly_forever()

    while True:
      try:
        self.turn_led_on(255, 100, 0)
        time.sleep(0.25)
        self.turn_led_off()
        time.sleep(0.25)
      except KeyboardInterrupt:
        self.relax()
        break

  def relax(self):
    self.stop()
    self.put_down()
    self.open_claw()
    self.turn_led_off()

  def add_claw(self, pin1=13, pin2=4, predef=None):
    if predef in ('SKRIBRAIN', 'SKRIBRAIN3'):
      self._claws.append(Claw(skribrain3.SERVO1, skribrain3.SERVO2))
    else:
      self._claws.append(Claw(pin1, pin2))

  def _add_dc_rotor(self, pin1, pin2, type):
    if type == 'LEFT':
      self._left_dc_rotors.append(DCRotor(pin1, pin2))
    elif type == 'RIGHT':
      self._right_dc_rotors.append(DCRotor(pin1, pin2))

  def add_dc_rotor(self, port, type):
    self._add_dc_rotor(port[0], port[1], type)

  def add_line_sensor(self, pin):
    self._qtrs.append(LineSensor(pin))

  def _add_distance_sensor(self, trig, echo):
    self._dist_sensors.append(DistanceSensor(trig, echo))

  def add_distance_sensor(self, port):
    self._add_distance_sensor(*port)

  def add_led(self, pin):
    self._leds.append(LED(pin))

  # Small Head
  def turn_led_on(self, r, g, b, pin=None):
    if pin is None:
      for led in self._leds:
        led.on(r, g, b)
    else:
      led = [l for l in self._leds if l.pin == pin][0]
      led.on(r, g, b)

  def turn_led_off(self, pin=None):
    self.TurnLEDOn(0, 0, 0, pin)

  # Movement
  def set_speed(self, speed):
    self.speed = speed

  def face_left(self, ms=None):
    for rotor in self._left_dc_rotors:
      rotor.move_backward(self.normspeed)

    for rotor in self._right_dc_rotors:
      rotor.move_forward(self.normspeed)

    if ms is not None:
      self._delay(ms)

  def face_right(self, ms=None):
    for rotor in self._left_dc_rotors:
      rotor.move_forward(self.normspeed)

    for rotor in self._right_dc_rotors:
      rotor.move_backward(self.normspeed)

    if ms is not None:
      self._delay(ms)

  def turn_left(self, ms=None):
    for rotor in self._left_dc_rotors:
      rotor.stop()

    for rotor in self._right_dc_rotors:
      rotor.move_forward(self.normspeed)

    if ms is not None:
      self._delay(ms)

  def turn_right(self, ms=None):
    for rotor in self._left_dc_rotors:
      rotor.move_forward(self.normspeed)

    for rotor in self._right_dc_rotors:
      rotor.stop()

    if ms is not None:
      self._delay(ms)

  def move_forward(self, ms=None):
    for rotor in self._dc_rotors:
      rotor.move_forward(self.normspeed)

    if ms is not None:
      self._delay(ms)

  def move_backward(self, ms=None):
    for rotor in self._dc_rotors:
      rotor.move_backward(self.normspeed)

    if ms is not None:
      self._delay(ms)

  def move_slowly_forever(self):
    for rotor in self._dc_rotors:
      rotor.move_forward(0.1)

  def stop(self):
    for rotor in self._dc_rotors:
      rotor.stop()

  # Gripper
  def close_claw(self):
    for claw in self._claws:
      claw.close()

  def open_claw(self):
    for claw in self._claws:
      claw.open()

  def pick_up(self):
    for claw in self._claws:
      claw.pick_up()

  def put_down(self):
    for claw in self._claws:
      claw.put_down()

  # Ultrasonic sensor
  def read_distance_sensor(self, pins):
    sensor = [s for s in self._dist_sensors if s.pins == pins][0]
    return sensor.read()

  # QTR
  def read_line_sensor(self, pin):
    qtr = [q for q in self._qtrs if q.pin == pin][0]
    return qtr.read()

  # Arduino Skribot.h compatibility wrappers
  def Configure_Connections(self, *args, **kwargs):
    self.configure_connections(*args, **kwargs)

  def set_speed(self, val):
    self.speed = val

  def SetSpeed(self, val):
    self.speed = val

  def OpenClaw(self):
    self.open_claw()

  def CloseClaw(self):
    self.close_claw()

  def Pick_Up(self):
    self.pick_up()

  def Put_Down(self):
    self.put_down()

  def TurnLEDOn(self, *args, **kwargs):
    self.turn_led_on(*args, **kwargs)

  def TurnLEDOff(self, *args, **kwargs):
    self.turn_led_off(*args, **kwargs)

  def Stop(self):
    self.stop()

  def MoveForward(self, *args, **kwargs):
    self.move_forward(*args, **kwargs)

  def MoveBack(self, *args, **kwargs):
    self.move_backward(*args, **kwargs)

  def TurnLeft(self, *args, **kwargs):
    self.turn_left(*args, **kwargs)

  def TurnRight(self, *args, **kwargs):
    self.turn_right(*args, **kwargs)

  def FaceLeft(self, *args, **kwargs):
    self.face_left(*args, **kwargs)

  def FaceRight(self, *args, **kwargs):
    self.face_right(*args, **kwargs)

  def ReadLineSensor(self, *args, **kwargs):
    return self.read_line_sensor(*args, **kwargs)

  def ReadDistSensor(self, *args, **kwargs):
    return self.read_distance_sensor(*args, **kwargs)

  def AddClaw(self, *args, **kwargs):
    self.add_claw(*args, **kwargs)

  def AddDCRotor(self, *args, **kwargs):
    self.add_dc_rotor(*args, **kwargs)

  def AddLineSensor(self, *args, **kwargs):
    self.add_line_sensor(*args, **kwargs)

  def AddDistSensor(self, *args, **kwargs):
    self.add_distance_sensor(*args, **kwargs)

  def AddLED(self, *args, **kwargs):
    self.add_led(*args, **kwargs)
