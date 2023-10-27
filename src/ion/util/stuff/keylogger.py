from pynput.keyboard import Listener
from .pynput_patcher import *
from .keys import ALL_KEYS, NUMBER_OF_KEYS
from .focus_checker import FocusChecker
from .common import print_debug

class KeyLogger:
  _listener: Listener = None
  _check_focus = None
  _focused = False
  _keyboard_state = {}
  _error = None

  @staticmethod
  def __init__():
    """
    Start the KeyLogger.
    This is a global instance, so the constructor cannot be called again until after calling .stop().
    """
    if KeyLogger.is_running(): raise RuntimeError("KeyLogger already running")

    def on_press(key):
      if key is None: return # because the key can be None in some cases

      print_debug("Pressed", key)
      if hasattr(key, "char"): key = key.char
      try: KeyLogger._focused = KeyLogger._check_focus()
      except BaseException as e:
        # an error occurs while checking focus, so pass this error to the main thread
        KeyLogger.stop()
        KeyLogger._error = e
        return False

      if KeyLogger._focused:
        for i in range(NUMBER_OF_KEYS):
          k = ALL_KEYS[i]["key"]
          if (k == key or (type(k) in (list, tuple) and any([i == key for i in k]))):
            KeyLogger.set_key(ALL_KEYS[i]["code"], True)

    def on_release(key):
      if key is None: return # because the key can be None is some cases

      print_debug("Released", key)
      if hasattr(key, "char"): key = key.char

      for i in range(NUMBER_OF_KEYS):
        k = ALL_KEYS[i]["key"]
        if (k == key or (type(k) in (list, tuple) and any([i == key for i in k]))):
          KeyLogger.set_key(ALL_KEYS[i]["code"], False)

    KeyLogger._error = None # remove errors
    KeyLogger._keyboard_state = {k["code"]: False for k in ALL_KEYS}
    KeyLogger._check_focus = FocusChecker()
    KeyLogger._listener = Listener(on_press=on_press, on_release=on_release)
    KeyLogger._listener.start()

  @staticmethod
  def raise_if_error():
    if KeyLogger._error:
      error = KeyLogger._error
      KeyLogger._error = None # remove the last error after raised it
      raise error

  @staticmethod
  def stop():
    """Stop the KeyLogger"""

    if KeyLogger._listener: KeyLogger._listener.stop()
    KeyLogger._listener = None
    KeyLogger._check_focus = None
    KeyLogger._focused = False
    KeyLogger._keyboard_state = {}

  @staticmethod
  def is_running():
    return KeyLogger._listener and KeyLogger._listener.is_alive()

  @staticmethod
  def get_key(code):
    """Get state of a key (is pressed or not) with his keycode"""

    if not KeyLogger.is_running(): raise RuntimeError("KeyLogger not running")
    elif type(code) != int: raise TypeError(f"keycode must be an integer, not {type(code).__name__}")
    elif code not in KeyLogger._keyboard_state: raise IndexError(f"key with code '{code}' not found")
    return KeyLogger._focused and KeyLogger._keyboard_state[code]

  @staticmethod
  def set_key(code, is_pressed, add=False):
    """Set state of a key with his keycode"""

    if not KeyLogger.is_running(): raise RuntimeError("KeyLogger not running")
    elif type(code) != int: raise TypeError(f"keycode must be an integer, not {type(code).__name__}")
    elif not add and code not in KeyLogger._keyboard_state: raise IndexError(f"key with code '{code}' not found")
    KeyLogger._keyboard_state[code] = bool(is_pressed)
