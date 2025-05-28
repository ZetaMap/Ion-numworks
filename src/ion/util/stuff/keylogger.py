from pynput.keyboard import Listener, Key, KeyCode, _NORMAL_MODIFIERS # hidden by __init__.py

from .pynput_patcher import *
from .keys import ALL_KEYS, ALL_KEYS_UNORDERED, ALL_HOTKEYS
from .focus_checker import FocusChecker
from .common import print_debug

# NOTE: the 'keycode' means the Numworks keyboard keycode, not a real keyboard keycode


class KeyLogger:
  _listener: Listener = None
  _check_focus: FocusChecker = None
  _focused = False
  _keyboard_state: dict[int, bool] = {}
  _error = None

  def __init__(self):
    raise NotImplementedError("singleton class")

  @staticmethod
  def _normalize_key(key):
    # We `.lower()` it, so that holding shift or having caplock enabled does not disable letter-binded keys.
    if type(key) == KeyCode and key.char is not None: return key.char.lower()
    # Try to normalize the modifier. E.g. Key.ctrl_r -> Key.ctrl
    elif type(key) == Key: return _NORMAL_MODIFIERS.get(key.value, key)
    return key
  
  @staticmethod
  def _on_press(key):
    try:  
      if key is None: return # because the key can be None in some cases
      print_debug("Pressed", key)
      key = KeyLogger._normalize_key(key)

      KeyLogger._focused = KeyLogger._check_focus()
      if not KeyLogger._focused: return
      
      k = ALL_KEYS_UNORDERED.get(key)
      if k is None: return
      KeyLogger.set_pressed(k["code"], True)
      
      # Handle hotkeys
      for h in ALL_HOTKEYS:
        if all(KeyLogger.is_pressed(ALL_KEYS_UNORDERED.get(k)["code"], no_check=True) for k in h["key"]):
          KeyLogger.set_pressed(h["code"], True, no_check=True)
          # Suppress the binded keys
          for k in h["key"]: KeyLogger.set_pressed(ALL_KEYS_UNORDERED.get(k)["code"], False, no_check=True)
          
    except BaseException as e:
      KeyLogger._error = e
      KeyLogger.stop()
      return

  @staticmethod
  def _on_release(key):
    try: 
      if key is None: return # because the key can be None is some cases
      print_debug("Released", key)
      key = KeyLogger._normalize_key(key)

      k = ALL_KEYS_UNORDERED.get(key)
      if k is None: return
      KeyLogger.set_pressed(k["code"], False)

      # Handle hotkeys
      for h in ALL_HOTKEYS:
        if KeyLogger.is_pressed(h["code"], no_check=True) and key in h["key"]:
          KeyLogger.set_pressed(h["code"], False, no_check=True)
          # Restore the binded keys
          for k in h["key"]: 
            if k != key: KeyLogger.set_pressed(ALL_KEYS_UNORDERED.get(k)["code"], True, no_check=True)
          
    except BaseException as e:
      KeyLogger._error = e
      KeyLogger.stop()
      return

  @staticmethod
  def start():
    """
    Start the KeyLogger.
    Cannot be called twice without calling .stop() first.
    """

    if KeyLogger.is_running(): raise RuntimeError("KeyLogger is already running")

    KeyLogger._error = None # remove last error
    KeyLogger._keyboard_state = {k["code"]: False for k in ALL_KEYS}
    KeyLogger._check_focus = FocusChecker()
    KeyLogger._listener = Listener(KeyLogger._on_press, KeyLogger._on_release)
    KeyLogger._listener.start()

  @staticmethod
  def stop():
    """Stop the KeyLogger"""

    if not KeyLogger.is_running(): return
    if KeyLogger._listener: KeyLogger._listener.stop()
    KeyLogger._listener = None
    KeyLogger._check_focus = None
    KeyLogger._focused = False
    KeyLogger._keyboard_state = {}

  @staticmethod
  def is_running():
    """Return whether the KeyLogger is running"""

    return KeyLogger._listener and KeyLogger._listener.is_alive()

  def raise_if_error():
    """Raise the last error"""

    if KeyLogger._error:
      error = KeyLogger._error
      KeyLogger._error = None # remove the last error after raised it
      raise error

  @staticmethod
  def check_ok(code):
    """Check the Keylogger state, the keycode and the focus"""

    KeyLogger.raise_if_error()
    if not KeyLogger.is_running(): raise RuntimeError("KeyLogger not running")
    elif type(code) != int: raise TypeError(f"keycode must be an integer, not {type(code).__name__}")
    elif code not in KeyLogger._keyboard_state: raise IndexError(f"key with code '{code}' not found")
    try: KeyLogger._check_focus.available()
    except:
      KeyLogger.stop()
      raise

  @staticmethod
  def is_pressed(code, *, no_check=False):
    """
    Get state of a key (is pressed or not) with his keycode. 
    
    Note: using no_check is insecure
    """

    if not no_check: KeyLogger.check_ok(code)
    return KeyLogger._focused and KeyLogger._keyboard_state[code]

  @staticmethod
  def set_pressed(code, is_pressed, *, no_check=False):
    """
    Set state of a key with his keycode.
    
    Note: using no_check is insecure
    """

    if not no_check: KeyLogger.check_ok(code)
    KeyLogger._keyboard_state[code] = bool(is_pressed)
