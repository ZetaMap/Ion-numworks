"""
This is just a little low level library for fetching keyboard input.
This is a porting of the Numworks module, and add other methods created by others OS (like Omega or Upsilon).
"""

try: from .util.ion import Ion as __Ion, OS_MODE
except ImportError as e:
  if "relative import" not in e.msg: 
    raise
  from util.ion import Ion as __Ion, OS_MODE

__name__ = "ion"
__version__ = "2.0"
try: 
  with open("README.md") as f: __doc__ = f.read()
  del f
except (FileNotFoundError, OSError): __doc__ = "<unknown>"
__all__ = [
  "keydown",
  "get_keys",
  "battery",
  "battery_level",
  "battery_ischarging",
  "set_brightness",
  "get_brightness",
  "file", # idk what is this
]


### All keys of Numworks
try: from .util.stuff.keys import *
except ImportError as e:
  if "relative import" not in e.msg: 
    raise
  from util.stuff.keys import *
# Add all keys in __all__
__all__.extend([i for i in dir() if i.startswith("KEY_")])


### Methods
def keydown(k, /):
  """Return True if the k key is pressed (not release)"""
  key, err = __Ion.call(__Ion.keydown, k)
  if err != None:
    raise err
  return key

def get_keys():
  """Get name of pressed keys"""
  keys, err = __Ion.call(__Ion.get_keys)
  if err != None:
    raise err
  return keys

# All the following functions only give a fake result to give a real look of library
def battery():
  """Return battery voltage"""
  voltage, err = __Ion.call(__Ion.battery)
  if err != None:
    raise err
  return voltage

def battery_level():
  """Return battery level"""
  level, err = __Ion.call(__Ion.battery_level)
  if err != None:
    raise err
  return level

def battery_ischarging():
  """Return True if the battery is charging"""
  charging, err = __Ion.call(__Ion.battery_ischarging)
  if err != None:
    raise err
  return charging

def set_brightness(level, /):
  """Set brightness level of screen"""
  _, err = __Ion.call(__Ion.set_brightness, level)
  if err != None:
    raise err

def get_brightness():
  """Get brightness level of screen"""
  brightness, err = __Ion.call(__Ion.get_brightness)
  if err != None:
    raise err
  return brightness

# I don't know why this exist, but is in source code of Omega and Upsilon
class file:
  SEEK_SET = 0
  SEEK_CUR = 1
  SEEK_END = 2
  def __init__(self, *_, **__): 
    raise \
      TypeError(f"cannot create '{self.__class__.__name__}' instances")


### Cleanup
if OS_MODE:
  if OS_MODE < 3:
    del get_keys, battery, battery_level, battery_ischarging, set_brightness, get_brightness
    __all__.remove("battery")
    __all__.remove("battery_level")
    __all__.remove("battery_ischarging")
    __all__.remove("set_brightness")
    __all__.remove("get_brightness")

  if OS_MODE == 1:
    del file
    __all__.remove("file")
del OS_MODE
