from os import environ
from random import randint, random

__all__ = ["Ion"]

class Ion:
  # '0': PC, '1': Numworks, '2': Omega, '3': Upsilon
  OS_MODE = environ.get('KANDINSKY_OS_MODE')
  if OS_MODE and OS_MODE.isdecimal(): OS_MODE = int(OS_MODE) if 0 <= int(OS_MODE) < 4 else 1

  brightness = 240

  def keydown(k, /):
    return False
    #TODO: make this

  def get_keys():
    return set()
    #TODO: make this

  # All the following functions only give a fake result to give a real look of library
  battery = lambda: 4.20+randint(900, 1500)/10**5+random()/10**5
  battery_level = lambda: 3
  battery_ischarging = lambda: True
  def set_brightness(level): Ion.brightness = 240 if level%256 > 240 else level%256
  get_brightness = lambda: Ion.brightness

  # Caller
  def call(method, *args, **kwargs):
    try: return method(*args, **kwargs), None
    except BaseException as e: return None, e.with_traceback(None)