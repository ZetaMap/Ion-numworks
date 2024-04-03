from os import environ
from random import randint, random

from .stuff.keylogger import *
from .stuff.keys import ALL_KEYS
from .stuff.common import *


# Enable debug
DEBUG = "ION_ENABLE_DEBUG" in environ
set_debug(DEBUG)

# Disable warnings
WARNINGS = "ION_DISABLE_WARNINGS" not in environ
set_warnings(WARNINGS)

# '0': PC, '1': Numworks, '2': Omega, '3': Upsilon
OS_MODE = environ.get('KANDINSKY_OS_MODE') or environ.get('ION_OS_MODE')
OS_MODE = (int(OS_MODE) if 0 <= int(OS_MODE) < 4 else 1) if OS_MODE and OS_MODE.isdecimal() else 1

# Check version of kandinsky to print an warning if is 'too old'
try:
  import importlib.metadata
  kandinsky_version = importlib.metadata.metadata("kandinsky").get_all("version")
  if kandinsky_version is None:
    prettywarn("invalid kandinsky metadata, are you sure the right library is installed?", DeprecationWarning)
  elif tuple([int(i) for i in kandinsky_version[0].split('.') if i.isdecimal()]) < (2, 5):
    prettywarn("for more stability, is recommended to upgrade kandinsky", DeprecationWarning)
  del importlib
except: pass


__all__ = ["Ion"]

class Ion:
  KeyLogger() # Start the key logger
  brightness = 240

  def keydown(k):
    if type(k) != int: raise TypeError(f"can't convert {type(k).__name__} to int")
    try: return KeyLogger.get_key(k)
    except IndexError: return False

  def get_keys():
    return set([k["name"] for k in ALL_KEYS if KeyLogger.get_key(k["code"])])

  # All the following functions only give a fake result to give a real look of library
  def battery(): return 4.20+randint(900, 1500)/10**5+random()/10**5
  def battery_level(): return 3
  def battery_ischarging(): return True
  def set_brightness(level):
    if type(level) != int: raise TypeError(f"can't convert {type(level).__name__} to int")
    Ion.brightness = 240 if level%256 > 240 else level%256
  def get_brightness(): return Ion.brightness

  # Caller
  def call(method, *args, **kwargs):
    try:
      print_debug("Event", method.__name__, (*args, *[f"{k}={repr(v)}" for k, v in kwargs.items()]), sep='')
      KeyLogger.raise_if_error() # raise the last KeyLogger error to main thread
      return method(*args, **kwargs), None
    except BaseException as e:
      return None, Exception.with_traceback(
        KeyboardInterrupt(type(e).__name__+": "+' '.join(e.args)) if isinstance(e, RuntimeError) else e,
        e.__traceback__.tb_next if DEBUG else None)
