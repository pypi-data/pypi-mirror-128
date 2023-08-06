from setuptools import setup

with open('requirements.txt', 'r') as f:
  requirements = f.read().splitlines()

with open('README.md', 'r') as f:
  long_description = f.read()

setup(
  name='thonny-skriware',
  description='Thonny plugin for programming Skribots - educational robots',
  long_description=long_description,
  long_description_content_type='text/markdown',
  url='https://skriware.com/robots/skribots',
  version='0.1.3',
  license='MIT',
  packages=['thonnycontrib.skriware'],
  include_package_data=True,
  package_data={
    'thonnycontrib.skriware': [
      'settings.json',
      'icons/*.png',
      'micropython-skribot/firmware.bin',
      'micropython-skribot/boot.py',
      'micropython-skribot/scratchpad.py',
      'micropython-skribot/example_*.py',
      'micropython-skribot/claw.py',
      'micropython-skribot/dc_rotor.py',
      'micropython-skribot/distance_sensor.py',
      'micropython-skribot/led.py',
      'micropython-skribot/line_sensor.py',
      'micropython-skribot/servo.py',
      'micropython-skribot/skribot.py',
      'micropython-skribot/skribrain.py',
      'micropython-skribot/skribrain3.py',
    ]
  },
  classifiers=[
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Plugins',
    'Intended Audience :: Education',
    'Intended Audience :: End Users/Desktop',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: MicroPython',
    'Topic :: Education',
    'Topic :: Software Development :: Embedded Systems',
  ],
  install_requires=requirements
)
