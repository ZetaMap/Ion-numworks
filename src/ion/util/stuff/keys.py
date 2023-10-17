from pynput.keyboard import Key

KEY_LEFT =             {'code': 0,  'name': 'left',      'key': Key.left}
KEY_UP =               {'code': 1,  'name': 'up',        'key': Key.up}
KEY_DOWN =             {'code': 2,  'name': 'down',      'key': Key.down}
KEY_RIGHT =            {'code': 3,  'name': 'right',     'key': Key.right}
KEY_OK =               {'code': 4,  'name': 'OK',        'key': Key.enter}
KEY_BACK =             {'code': 5,  'name': 'back',      'key': Key.delete}
KEY_HOME =             {'code': 6,  'name': 'home',      'key': Key.esc}
KEY_ONOFF =            {'code': 7,  'name': 'onOff',     'key': Key.end}
KEY_SHIFT =            {'code': 12, 'name': 'shift',     'key': (Key.shift_l, Key.shift_r)}
KEY_ALPHA =            {'code': 13, 'name': 'alpha',     'key': (Key.ctrl_l, Key.ctrl_r)}
KEY_XNT =              {'code': 14, 'name': 'xnt',       'key': 'x'}
KEY_VAR =              {'code': 15, 'name': 'var',       'key': 'v'}
KEY_TOOLBOX =          {'code': 16, 'name': 'toolbox',   'key': '"'}
KEY_BACKSPACE =        {'code': 17, 'name': 'backspace', 'key': Key.backspace}
KEY_EXP =              {'code': 18, 'name': 'exp',       'key': 'e'}
KEY_LN =               {'code': 19, 'name': 'ln',        'key': 'n'}
KEY_LOG =              {'code': 20, 'name': 'log',       'key': 'l'}
KEY_IMAGINARY =        {'code': 21, 'name': 'imaginary', 'key': 'i'}
KEY_COMMA =            {'code': 22, 'name': 'comma',     'key': ','}
KEY_POWER =            {'code': 23, 'name': 'power',     'key': '^'}
KEY_SINE =             {'code': 24, 'name': 'sin',       'key': 's'}
KEY_COSINE =           {'code': 25, 'name': 'cos',       'key': 'c'}
KEY_TANGENT =          {'code': 26, 'name': 'tan',       'key': 't'}
KEY_PI =               {'code': 27, 'name': 'pi',        'key': 'p'}
KEY_SQRT =             {'code': 28, 'name': 'sqrt',      'key': 'r'}
KEY_SQUARE =           {'code': 29, 'name': 'square',    'key': '>'}
KEY_SEVEN =            {'code': 30, 'name': '7',         'key': '7'}
KEY_EIGHT =            {'code': 31, 'name': '8',         'key': '8'}
KEY_NINE =             {'code': 32, 'name': '9',         'key': '9'}
KEY_LEFTPARENTHESIS =  {'code': 33, 'name': '(',         'key': '('}
KEY_RIGHTPARENTHESIS = {'code': 34, 'name': ')',         'key': ')'}
KEY_FOUR =             {'code': 36, 'name': '4',         'key': '4'}
KEY_FIVE =             {'code': 37, 'name': '5',         'key': '5'}
KEY_SIX =              {'code': 38, 'name': '6',         'key': '6'}
KEY_MULTIPLICATION =   {'code': 39, 'name': '*',         'key': '*'}
KEY_DIVISION =         {'code': 40, 'name': '/',         'key': '/'}
KEY_ONE =              {'code': 42, 'name': '1',         'key': '1'}
KEY_TWO =              {'code': 43, 'name': '2',         'key': '2'}
KEY_THREE =            {'code': 44, 'name': '3',         'key': '3'}
KEY_PLUS =             {'code': 45, 'name': '+',         'key': '+'}
KEY_MINUS =            {'code': 46, 'name': '-',         'key': '-'}
KEY_ZERO =             {'code': 48, 'name': '0',         'key': '0'}
KEY_DOT =              {'code': 49, 'name': '.',         'key': '.'}
KEY_EE =               {'code': 50, 'name': 'EE',        'key': '!'}
KEY_ANS =              {'code': 51, 'name': 'Ans',       'key': 'a'}
KEY_EXE =              {'code': 52, 'name': 'EXE',       'key': Key.insert}# TODO: not on macos, find another key

# Put all keys in ALL_KEYS and redefine each key only by its code
ALL_KEYS = []

for n, k in locals().copy().items():
  # Avoid to re-replace variable if file is imported at multiple times
  if n.startswith("KEY_") and type(k) == dict:
    k.update({'field': n})
    locals()[n] = k['code']
    ALL_KEYS.append(k)

NUMBER_OF_KEYS = len(ALL_KEYS)
__all__ = [k['field'] for k in ALL_KEYS]
