KEY_LEFT: int    = 0
KEY_UP: int      = 1
KEY_DOWN: int    = 2
KEY_RIGHT: int   = 3
KEY_OK: int      = 4
KEY_BACK: int    = 5
KEY_HOME: int    = 6
KEY_ONOFF: int   = 7
KEY_SHIFT: int   = 12
KEY_ALPHA: int   = 13
KEY_XNT: int     = 14
KEY_VAR: int     = 15
KEY_TOOLBOX: int    = 16
KEY_BACKSPACE: int  = 17
KEY_EXP: int     = 18
KEY_LN: int      = 19
KEY_LOG: int     = 20
KEY_IMAGINARY: int  = 21
KEY_COMMA: int   = 22
KEY_POWER: int   = 23
KEY_SINE: int    = 24
KEY_COSINE: int  = 25
KEY_TANGENT: int = 26
KEY_PI: int      = 27
KEY_SQRT: int    = 28
KEY_SQUARE: int  = 29
KEY_SEVEN: int   = 30
KEY_EIGHT: int   = 31
KEY_NINE: int    = 32
KEY_LEFTPARENTHESIS: int  = 33
KEY_RIGHTPARENTHESIS: int = 34
KEY_FOUR: int    = 36
KEY_FIVE: int    = 37
KEY_SIX: int     = 38
KEY_MULTIPLICATION: int   = 39
KEY_DIVISION: int         = 40
KEY_ONE: int     = 42
KEY_TWO: int     = 43
KEY_THREE: int   = 44
KEY_PLUS: int    = 45
KEY_MINUS: int   = 46
KEY_ZERO: int    = 48
KEY_DOT: int     = 49
KEY_EE: int      = 50
KEY_ANS: int     = 51
KEY_EXE: int     = 52

def keydown(k: int, /) -> bool: ...
def get_keys() -> set[str]: ...
def battery() -> int: ...
def battery_level() -> int: ...
def battery_ischarging() -> int: ...
def set_brightness(level: int, /) -> None: ...
def get_brightness() -> int: ...

class file:
  SEEK_SET: int = 0
  SEEK_CUR: int = 1
  SEEK_END: int = 2
  def __init__() -> None: ...
