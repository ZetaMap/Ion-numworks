"""
Patch Pynput to add support of Caps Lock modifier.
"""

import sys, os

__all__ = []

pynput_backend = os.environ.get(
        'PYNPUT_BACKEND_{}'.format(__name__.rsplit('.')[-1].upper()),
        os.environ.get('PYNPUT_BACKEND', None))
if not pynput_backend: pynput_backend = sys.platform


if pynput_backend == "dummy":
  # No patch
  pass


elif pynput_backend == "uinput":
  # Idk how to test this but I hope this work
  from pynput.keyboard._uinput import Listener, Key, KeyEvent

  Listener.last_capslock_state = KeyEvent.key_up
  Listener__handle_original = Listener._handle

  def Listener__handle(self, event):
    if event.code == Key.caps_lock.value.vk:
      if event.value == KeyEvent.key_down and Listener.last_capslock_state == KeyEvent.key_up:
        if Key.shift in self._modifiers: self._modifiers.remove(Key.shift)
        else: self._modifiers.add(Key.shift)
      Listener.last_capslock_state = event.value
    Listener__handle_original(self, event)

  Listener._handle = Listener__handle


elif pynput_backend == "darwin":
  # TODO: make support
  ...


elif pynput_backend == "win32":
  # It's really poorly coded but it does the job, so I'm keeping it for now
  from pynput._util.win32 import KeyTranslator, VK, ctypes
  from pynput.keyboard._win32 import Listener

  class Capslock:
    """Class to store temporary variables for caps lock patch"""
    last_code = Listener._WM_KEYUP

    keyboard = (ctypes.c_ubyte * 255)()
    KeyTranslator._GetKeyboardState(ctypes.byref(keyboard))
    enabled = bool(keyboard[VK.CAPITAL])
    del keyboard

  Listener__convert_original = Listener._convert
  KeyTranslator__modifier_state_original = KeyTranslator._modifier_state

  def Listener__convert(self, code, msg, lpdata):
    """Wrap the hook callback to handle caps lock key code"""
    converted = Listener__convert_original(self, code, msg, lpdata)
    if converted and converted[1] == VK.CAPITAL:
      if converted[0] in Listener._PRESS_MESSAGES and converted[0] != Capslock.last_code:
        Capslock.enabled = not Capslock.enabled
      Capslock.last_code = converted[0]
    return converted
  
  def KeyTranslator__modifier_state(self):
    """Wrap the method to add the check of caps lock"""
    shift, ctrl, alt = KeyTranslator__modifier_state_original(self)
    if Capslock.enabled: shift = not shift
    return shift, ctrl, alt
  
  Listener._convert = Listener__convert
  KeyTranslator._modifier_state = KeyTranslator__modifier_state


else: # linux/xorg backend
  # For linux, this is more simple, just need to redefine one function to handle caps lock bit-mask
  import pynput.keyboard._xorg as xorg

  def shift_to_index(display, shift):
    return (          # |added thing|
        (1 if shift & 1 or shift & 3 else 0) +
        (2 if shift & xorg.alt_gr_mask(display) else 0))

  xorg.shift_to_index = shift_to_index
