from pynput.keyboard import Key
import sys # for macos compatibility

KEY_LEFT: int =             {'code': 0,  'name': 'left',      'key': Key.left}
KEY_UP: int =               {'code': 1,  'name': 'up',        'key': Key.up}
KEY_DOWN: int =             {'code': 2,  'name': 'down',      'key': Key.down}
KEY_RIGHT: int =            {'code': 3,  'name': 'right',     'key': Key.right}
KEY_OK: int =               {'code': 4,  'name': 'OK',        'key': Key.enter}
KEY_BACK: int =             {'code': 5,  'name': 'back',      'key': Key.delete}
KEY_HOME: int =             {'code': 6,  'name': 'home',      'key': Key.esc}
KEY_ONOFF: int =            {'code': 7,  'name': 'onOff',     'key': Key.end}
KEY_SHIFT: int =            {'code': 12, 'name': 'shift',     'key': Key.shift}
KEY_ALPHA: int =            {'code': 13, 'name': 'alpha',     'key': Key.ctrl}
KEY_XNT: int =              {'code': 14, 'name': 'xnt',       'key': 'x'}
KEY_VAR: int =              {'code': 15, 'name': 'var',       'key': 'v'}
KEY_TOOLBOX: int =          {'code': 16, 'name': 'toolbox',   'key': '"'}
KEY_BACKSPACE: int =        {'code': 17, 'name': 'backspace', 'key': Key.backspace}
KEY_EXP: int =              {'code': 18, 'name': 'exp',       'key': 'e'}
KEY_LN: int =               {'code': 19, 'name': 'ln',        'key': 'n'}
KEY_LOG: int =              {'code': 20, 'name': 'log',       'key': 'l'}
KEY_IMAGINARY: int =        {'code': 21, 'name': 'imaginary', 'key': 'i'}
KEY_COMMA: int =            {'code': 22, 'name': 'comma',     'key': ','}
KEY_POWER: int =            {'code': 23, 'name': 'power',     'key': '^'}
KEY_SINE: int =             {'code': 24, 'name': 'sin',       'key': 's'}
KEY_COSINE: int =           {'code': 25, 'name': 'cos',       'key': 'c'}
KEY_TANGENT: int =          {'code': 26, 'name': 'tan',       'key': 't'}
KEY_PI: int =               {'code': 27, 'name': 'pi',        'key': 'p'}
KEY_SQRT: int =             {'code': 28, 'name': 'sqrt',      'key': 'r'}
KEY_SQUARE: int =           {'code': 29, 'name': 'square',    'key': '>'}
KEY_SEVEN: int =            {'code': 30, 'name': '7',         'key': '7'}
KEY_EIGHT: int =            {'code': 31, 'name': '8',         'key': '8'}
KEY_NINE: int =             {'code': 32, 'name': '9',         'key': '9'}
KEY_LEFTPARENTHESIS: int =  {'code': 33, 'name': '(',         'key': '('}
KEY_RIGHTPARENTHESIS: int = {'code': 34, 'name': ')',         'key': ')'}
KEY_FOUR: int =             {'code': 36, 'name': '4',         'key': '4'}
KEY_FIVE: int =             {'code': 37, 'name': '5',         'key': '5'}
KEY_SIX: int =              {'code': 38, 'name': '6',         'key': '6'}
KEY_MULTIPLICATION: int =   {'code': 39, 'name': '*',         'key': '*'}
KEY_DIVISION: int =         {'code': 40, 'name': '/',         'key': '/'}
KEY_ONE: int =              {'code': 42, 'name': '1',         'key': '1'}
KEY_TWO: int =              {'code': 43, 'name': '2',         'key': '2'}
KEY_THREE: int =            {'code': 44, 'name': '3',         'key': '3'}
KEY_PLUS: int =             {'code': 45, 'name': '+',         'key': '+'}
KEY_MINUS: int =            {'code': 46, 'name': '-',         'key': '-'}
KEY_ZERO: int =             {'code': 48, 'name': '0',         'key': '0'}
KEY_DOT: int =              {'code': 49, 'name': '.',         'key': '.'}
KEY_EE: int =               {'code': 50, 'name': 'EE',        'key': '!'}
KEY_ANS: int =              {'code': 51, 'name': 'Ans',       'key': 'a'} # vv Insert doesn't exists on mac keyboards, so use shift+enter
KEY_EXE: int =              {'code': 52, 'name': 'EXE',       'key': (Key.shift, Key.enter) if sys.platform.startswith("darwin") else Key.insert}

# Put all keys in ALL_KEYS and redefine each key only by its code
ALL_KEYS = []
ALL_KEYS_UNORDERED = {}
ALL_HOTKEYS = []

for n, k in locals().copy().items():
  # Avoid to re-replace variable if file is imported at multiple times
  if n.startswith("KEY_") and type(k) == dict:
    k.update({'field': n})
    locals()[n] = k['code'] # TODO: it's a good way to do that?
    ALL_KEYS.append(k)
    ALL_KEYS_UNORDERED[k['key']] = k
    if type(k['key']) in (tuple, list): ALL_HOTKEYS.append(k)

NUMBER_OF_KEYS = len(ALL_KEYS)

__all__ = [k['field'] for k in ALL_KEYS]
