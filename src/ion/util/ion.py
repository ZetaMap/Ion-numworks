from os import environ
from random import randint, random
from .keylogger import *
from .keys import ALL_KEYS

# '0': PC, '1': Numworks, '2': Omega, '3': Upsilon
OS_MODE = environ.get('KANDINSKY_OS_MODE')
OS_MODE = (int(OS_MODE) if 0 <= int(OS_MODE) < 4 else 1) if OS_MODE and OS_MODE.isdecimal() else 1
del environ
# By default it just read kandinsky window (only if is focused)
USE_KANDINSKY_INPUT_ONLY = 'ION_DISABLE_KANDINSKY_INPUT_ONLY' not in environ

# Start the key logger
KeyLogger()


__all__ = ["Ion"]

class Ion:
  brightness = 240

  def keydown(k):
    if type(k) != int: raise TypeError(f"can't convert {type(k).__name__} to int")
    try: return KeyLogger.get_key(k)
    except IndexError: return False

  get_keys = lambda: set([k["name"] for k in ALL_KEYS if KeyLogger.get_key(k["code"])])
  
  # All the following functions only give a fake result to give a real look of library
  battery = lambda: 4.20+randint(900, 1500)/10**5+random()/10**5
  battery_level = lambda: 3
  battery_ischarging = lambda: True
  def set_brightness(level): 
    if type(level) != int: raise TypeError(f"can't convert {type(level).__name__} to int")
    Ion.brightness = 240 if level%256 > 240 else level%256
  get_brightness = lambda: Ion.brightness

  # Caller
  def call(method, *args, **kwargs):
    try: return method(*args, **kwargs), None
    except BaseException as e: return None, e.with_traceback(None)
