"""
This is the adaptation of Ion module of Numworks.
Please don't use keyboard and this module at the same time.
"""
### v All keys of Numworks v ###
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
KEYS = [
  "left", "up", "down", "right", "return", "del", "home", "end", None, None, 
  None, None, "shift", "ctrl", ":", ";", "\"", "backspace", "[", "]", 
  "{", "}", ", ", "^", "s", "c", "t", "p", "<", "²", 
  "7", "8", "9", "(", ")", None, "4", "5", "6", "*", 
  "/", None, "1", "2", "3", "+", "-", None, "0", ".", 
  "insert", "@", "enter"
]
### ^ All keys of Numworks ^ ###

from keyboard import is_pressed

def keydown(key):
  if key < 0 or key > 52 or KEYS[key] == None: return False
  else: return is_pressed(KEYS[key])

def get_keys(): return KEYS
