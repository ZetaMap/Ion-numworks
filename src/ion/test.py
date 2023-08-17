import os
os.environ['KANDINSKY_OS_MODE'] = '3'
from __init__ import *

while 1:
  k = get_keys()
  if k: print(k)


exit()
import pywinctl, pygame
pygame.init()
pygame.display.set_mode((400,400))
pygame.display.flip()
for i in pywinctl.getAllWindows():
  print(i, i._hWnd)

exit()

import ctypes, os


def GetFirstWindowFromThreadProcessId(pid, classname=None, not_classname=False, contains_title=None):
  if classname:
    if type(classname) in (list, tuple): pass
    elif type(classname) == str: classname = (classname,)
    else: raise TypeError("invalid type for class name")
  if contains_title and type(contains_title) != str: raise TypeError("invalid type for contains name")
  contains_title = contains_title.lower()
  
  def foreach_window(hwnd, _):
    lpdw = ctypes.c_uint()
    ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(lpdw))       
    buff = ctypes.create_unicode_buffer(256)
    ctypes.windll.user32.GetWindowTextW(hwnd, buff, 256)

    print(contains_title, [buff.value], lpdw.value)

    if lpdw.value == pid and ctypes.windll.user32.IsWindowVisible(hwnd):
      print(lpdw)
      if classname:
        buff = ctypes.create_unicode_buffer(256)
        ctypes.windll.user32.GetClassNameW(hwnd, buff)

        if not ((not_classname and any([buff.value != name for name in classname])) or
                (not not_classname and any([buff.value == name for name in classname]))): 
          return True
      
      if contains_title:
        buff = ctypes.create_unicode_buffer(256)
        ctypes.windll.user32.GetWindowTextW(hwnd, buff, 256)

        if contains_title not in buff.value.lower(): return True
            
      window.value = hwnd
      return False
    return True
  
  window = ctypes.c_uint(0)
  ctypes.windll.user32.EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_uint, ctypes.c_uint)(foreach_window), 0)
  return window.value


buff = ctypes.create_unicode_buffer(256)
ctypes.windll.kernel32.GetConsoleTitleW(buff, 256)
print(buff.value)
print(GetFirstWindowFromThreadProcessId(os.getpid(), contains_title=buff.value))
cwid = ctypes.windll.kernel32.GetConsoleWindow()
lpdw = ctypes.c_uint()
ctypes.windll.user32.GetWindowThreadProcessId(cwid, ctypes.byref(lpdw))  
print("console wid", cwid, ctypes.windll.user32.IsWindowVisible(cwid), lpdw.value)
exit()

from pynput import keyboard
from Xlib import X, display
from os import getpid

def get_window_by_pid(pid, classname=None, not_classname=False, contains_title=None):
    d = display.Display()
    root = d.screen().root # should loop over all screens
    wins = [root]

    while len(wins) != 0:
        win = wins.pop(0)
        wpid = win.get_full_property(d.get_atom('_NET_WM_PID'), X.AnyPropertyType)
        
        if wpid and pid == wpid.value[0] and win.get_attributes().map_state == X.IsViewable:  
          found = True

          if found and classname:
            wclass = win.get_full_property(d.get_atom('WM_CLASS'), X.AnyPropertyType)
            if wclass:
              wclass = wclass.value.decode("utf-8").split('\0')[1]
              if not ((not_classname and any([wclass != name for name in classname])) or
                      (not not_classname and any([wclass == name for name in classname]))): 
                found = False
            else: found = False

          if found and contains_title:
            wtitle = win.get_full_property(d.get_atom('_NET_WM_NAME'), X.AnyPropertyType)
            if not wtitle or contains_title not in wtitle.value.decode("utf-8").lower(): found = False

          if found: return win.id
        
        subwins = win.query_tree().children
        if subwins != None: wins += subwins

    return 0

import tkinter
tk = tkinter.Tk()
tk.eval('tk::PlaceWindow . center')
tk.update()
tk.update_idletasks()
get_window_by_pid(getpid())
exit()
# Fonction pour obtenir le nom de la fenêtre en focus
def get_focused_window_name():
    d = display.Display()
    wid = d.screen().root.get_full_property(d.get_atom('_NET_ACTIVE_WINDOW'), X.AnyPropertyType).value[0]
    win = d.create_resource_object('window', wid)
    return win.get_full_property(
      d.get_atom('_NET_WM_PID'), X.AnyPropertyType), wid

# Callback pour la détection des touches pressées
def on_press(key):
    # Obtenir le nom de la fenêtre en focus
    focused_window_name = get_focused_window_name()
    print(f"Touches pressées dans la fenêtre : {focused_window_name}")

print(get_focused_window_name())

# Ecouteur pour les touches pressées
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()



exit()
import ctypes, sys, os
from pynput.keyboard import Listener
from util.stuff.keys import ALL_KEYS, NUMBER_OF_KEYS

# By default it just read kandinsky window (only if is focused)
USE_KANDINSKY_INPUT_ONLY = 'ION_DISABLE_KANDINSKY_INPUT_ONLY' not in os.environ
# Option to get input everywhere on system
GET_INPUT_EVERYWHERE = 'ION_ENABLE_GET_INPUT_EVERYWHERE' in os.environ


class IFocusChecker:
  kandinsky_window_id = 0
  kandinsky_not_found_error_printed = False
  python_window_id = 0

  def __init__(self):
    if self.kandinsky_window_id == 0 and "kandinsky" in sys.modules:
      # To find kandinsky is more simple, no need to find parent processes with a valid window
      # 'TkTopLevel' is the class name of root tkinter window, 'pygame' because in old releases of kandinsky i used pygame
      self.kandinsky_window_id = self.bind_kandinsky_window()

      if self.kandinsky_window_id == 0 and not self.kandinsky_not_found_error_printed:
        # Kandinsky window not found
        print("could not find the kandinsky window to get inputs.", RuntimeWarning)
        self.kandinsky_not_found_error_printed = True

      if USE_KANDINSKY_INPUT_ONLY: 
        self.python_window_id = 0
        return

    if self.python_window_id == 0:
      # Find python cosole window and ignore the top level of tkinter
      self.python_window_id = self.bind_python_console()

  def __call__(self):
    # Verify is kandinsky is imported, for the first true test (if no error) this will re-init FocusChecker
    if self.kandinsky_window_id == 0 and "kandinsky" in sys.modules: self.__init__()
    return ((self.python_window_id and self.check_console_focus()) or
            (self.kandinsky_window_id and self.check_kandinsky_focus()))

  def bind_kandinsky_window(self) -> int:
    raise NotImplementedError
  
  def bind_python_console(self) -> int:
    raise NotImplementedError
  
  def check_kandinsky_focus(self) -> bool:
    raise NotImplementedError
    
  def check_console_focus(self) -> bool:
    raise NotImplementedError


import Xlib
class FocusChecker(IFocusChecker):
  def bind_kandinsky_window(self):
    ...

  def bind_python_console(self):
    ...

  def check_kandinsky_focus(self):
    ...
    
  def check_console_focus(self):
    ...


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


#from Xlib import display
import os, ctypes, tkinter, threading, time, Xlib
try: import gi
except ImportError as e:
  e.msg = "Missing dependency 'gi': please install it with command 'apt install python3-gi'"
  raise


def GetWindowsFromThreadProcessId(pid, class_name=None, not_class_name=False):
  windows = []
  display = Xlib.display.Display()
  screen = display.screen().root

  for window in screen.query_tree().children:
    wpid = 0
    for i in range(375):
      if i in (0, 5, 375, 386): continue
      k = window.get_property(i, Xlib.X.ParentRelative, 0, 0)
      if k: 
        print(window, pid, i, k)
        wpid = k._data['sequence_number']
    
    if pid == wpid: windows.append(window.id)
tt=threading.Thread(target=lambda: print(">>", tt.native_id, "<<") or tkinter.Tk().mainloop())
tt.start()

display = Xlib.display.Display()
screen = display.screen().root
print(display.intern_atom('_NET_CLIENT_LIST'), display.intern_atom('_NET_WM_PID'))
KeyLogger()

#import kandinsky 
#o=tkinter.Tk()
#buffer_ = ctypes.create_unicode_buffer(256)
#ctypes.windll.kernel32.GetConsoleTitleW(buffer_, 256)
print(os.getpid(), os.getppid(), GetWindowsFromThreadProcessId(os.getpid()))

while 1:
  k = set([k["name"] for k in ALL_KEYS if KeyLogger.get_key(k["code"])])
  if k: print(k)
