from pynput.keyboard import Listener
from .keys import ALL_KEYS, NUMBER_OF_KEYS
from .focus_checker import FocusChecker

class KeyLogger:
  _listener = None
  _check_focus = None
  _focused = False
  _keyboard_state = {}

  @staticmethod
  def __init__():
    if KeyLogger._listener is not None: raise RuntimeError("KeyLogger already created")

    def on_press(key):
      if hasattr(key, "char"): key = key.char
      KeyLogger._focused = KeyLogger._check_focus()

      if KeyLogger._focused:
        for i in range(NUMBER_OF_KEYS):
          k = ALL_KEYS[i]["key"]
          if (k == key or (type(k) in (list, tuple) and any([i == key for i in k]))): 
            KeyLogger.set_key(ALL_KEYS[i]["code"], True)

    def on_release(key):
      if hasattr(key, "char"): key = key.char

      for i in range(NUMBER_OF_KEYS):
        k = ALL_KEYS[i]["key"]
        if (k == key or (type(k) in (list, tuple) and any([i == key for i in k]))): 
          KeyLogger.set_key(ALL_KEYS[i]["code"], False)

    KeyLogger._keyboard_state = {k["code"]: False for k in ALL_KEYS}
    KeyLogger._check_focus = FocusChecker()
    KeyLogger._listener = Listener(on_press=on_press, on_release=on_release) 
    KeyLogger._listener.start()

  @staticmethod
  def get_key(code):
    """Get state of a key (is pressed or not) with his keycode"""

    if KeyLogger._listener is None: raise RuntimeError("KeyLogger not created")
    elif type(code) != int: raise TypeError(f"keycode must be an integer, not {type(code).__name__}")
    elif code not in KeyLogger._keyboard_state: raise IndexError(f"key with code '{code}' not found")
    return KeyLogger._focused and KeyLogger._keyboard_state[code]

  @staticmethod
  def set_key(code, is_pressed):
    """Set state of a key with his keycode"""

    if KeyLogger._listener is None: raise RuntimeError("KeyLogger not created")
    elif type(code) != int: raise TypeError(f"keycode must be an integer, not {type(code).__name__}")
    elif code not in KeyLogger._keyboard_state: raise IndexError(f"key with code '{code}' not found")
    KeyLogger._keyboard_state[code] = bool(is_pressed)
