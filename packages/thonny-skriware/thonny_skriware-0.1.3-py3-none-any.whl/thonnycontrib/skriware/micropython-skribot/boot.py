import time

from skribot import Skribot
from skribrain import * # pinout definition

# You can configure standard connections
# by replacing the following line with
# robot = Skribot(predef='SKRIBRAIN')
robot = Skribot(predef='SKRIBRAIN')

def setup():
    '''Put setup code here.'''

def loop():
    '''Put loop code here.'''
    robot.turn_led_on(255, 255, 255)
    time.sleep(1)
    robot.turn_led_off()
    time.sleep(1)

try:
    if (robot.app_switch and robot.app_switch.value()) or not robot.app_switch:
      setup()
      while True:
          loop()
except KeyboardInterrupt:
    pass
