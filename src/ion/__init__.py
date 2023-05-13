"""
This is just a little low level library for fetching keyboard input. <br>
This is a porting of the Numworks module, and add other methods created by others OS (like Omega or Upsilon).
"""

try: from .util.ion import Ion as __Ion
except ImportError as e:
  if "relative import" not in e.msg: 
    raise
  from util.ion import Ion as __Ion

__name__ = "ion"
__version__ = "2.0"
try: __doc__ = open("README.md").read()
except (FileNotFoundError, OSError): __doc__ = "<unknown>"
__all__ = [
  "keydown",
  "get_keys",
  "battery",
  "battery_level",
  "battery_ischarging",
  "set_brightness",
  "get_brightness",
]


### All keys of Numworks
KEY_LEFT = 0
KEY_UP = 1
KEY_DOWN = 2
KEY_RIGHT = 3
KEY_OK = 4
KEY_BACK = 5
KEY_HOME = 6
KEY_ONOFF = 7
KEY_SHIFT = 12
KEY_ALPHA = 13
KEY_XNT = 14
KEY_VAR = 15
KEY_TOOLBOX = 16
KEY_BACKSPACE = 17
KEY_EXP = 18
KEY_LN = 19
KEY_LOG = 20
KEY_IMAGINARY = 21
KEY_COMMA = 22
KEY_POWER = 23
KEY_SINE = 24
KEY_COSINE = 25
KEY_TANGENT = 26
KEY_PI = 27
KEY_SQRT = 28
KEY_SQUARE = 29
KEY_SEVEN = 30
KEY_EIGHT = 31
KEY_NINE = 32
KEY_LEFTPARENTHESIS = 33
KEY_RIGHTPARENTHESIS = 34
KEY_FOUR = 36
KEY_FIVE = 37
KEY_SIX = 38
KEY_MULTIPLICATION = 39
KEY_DIVISION = 40
KEY_ONE = 42
KEY_TWO = 43
KEY_THREE = 44
KEY_PLUS = 45
KEY_MINUS = 46
KEY_ZERO = 48
KEY_DOT = 49
KEY_EE = 50
KEY_ANS = 51
KEY_EXE = 52
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
  def __init__(*_, **__): 
    raise \
      TypeError("cannot create 'file' instances")


### Cleanup
if __Ion.OS_MODE:
  if __Ion.OS_MODE < 3:
    del get_keys, battery, battery_level, battery_ischarging, set_brightness, get_brightness
    __all__.remove("battery")
    __all__.remove("battery_level")
    __all__.remove("battery_ischarging")
    __all__.remove("set_brightness")
    __all__.remove("get_brightness")

  if __Ion.OS_MODE == 1:
    del file
