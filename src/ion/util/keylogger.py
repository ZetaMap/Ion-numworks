import sys, os
from pynput.keyboard import Listener
from keys import ALL_KEYS, NUMBER_OF_KEYS

# By default it just read kandinsky window (only if is focused)
USE_KANDINSKY_INPUT_ONLY = 'ION_DISABLE_KANDINSKY_INPUT_ONLY' not in os.environ

if os.name == "nt":
  import ctypes

  def GetFirstWindowFromThreadProcessId(pid, class_name=None, not_class_name=False):
    window = ctypes.c_uint()
    
    def foreach_window(hwnd, _):
      lpdw = ctypes.c_uint()
      ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(lpdw))
      
      if lpdw.value == pid and ctypes.windll.user32.IsWindowVisible(hwnd):
        if class_name:
          buff = ctypes.create_unicode_buffer(256)
          ctypes.windll.user32.GetClassNameW(hwnd, buff)

          if not ((not_class_name and buff.value != class_name) or
                  (not not_class_name and buff.value == class_name)
                  ):
            return True

        window.value = hwnd
        return False
      return True
    
    ctypes.windll.user32.EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_uint, ctypes.c_uint)(foreach_window), 0)
    return window.value

  class FocusChecker:
    kandinsky_window_id = 0
    python_window_id = 0

    def __init__(self):
      if self.kandinsky_window_id == 0 and "kandinsky" in sys.modules:
        #To find kandinsky is more simple, no need to find parent processes with a valid window
        # 'TkTopLevel' is the class name of root tkinter window
        self.kandinsky_window_id = GetFirstWindowFromThreadProcessId(os.getpid(), "TkTopLevel")

        if USE_KANDINSKY_INPUT_ONLY: 
          self.python_window_id = 0
          return


      if self.python_window_id == 0:
        # Find python cosole window and ignore the top level of tkinter
        self.python_window_id = GetFirstWindowFromThreadProcessId(os.getpid(), "TkTopLevel", True)

        if self.python_window_id == 0:
          # Python probably started by another process, in this mode python don't have 'real' window
          # So try going back in the parent processes to find a valid window
          ppid = os.getppid()
          for _ in range(20): # Loop limit to avoid infinite loop
            self.python_window_id = GetFirstWindowFromThreadProcessId(ppid, "TkTopLevel", True)

            # Found an valid window
            if self.python_window_id: break

            # Not found at this time, try with his ppid
            from subprocess import check_output, CalledProcessError # need this because calling 'wmic' directly
            try: result = [i for i in check_output(['wmic', 'process', 'where', f'ProcessId={ppid}', 'get', 'ParentProcessId']).decode().splitlines() if i.strip() != '']
            except CalledProcessError: continue # Error happening, will try again in the next iteration

            if len(result) == 1:
              # No parent found, parent died or idk
              print("RuntimeWarning: cannot find an valid window to get input from python console.")
              break
            else: ppid = int(result[1].strip())

          else: 
            # No valid parent window found!
            # Python probably started in no-shell-mode and/or by a task
            # So will not log python console input
            print("RuntimeWarning: cannot find an valid window to get input from python console.")

    def __call__(self):
      # Verify is kandinsky is imported, for the first true test this will re-init the FocusChecker
      if self.kandinsky_window_id == 0 and "kandinsky" in sys.modules: self.__init__()

      fgw = ctypes.windll.user32.GetForegroundWindow()
      return ((self.python_window_id and fgw == self.python_window_id) or 
              (self.kandinsky_window_id and fgw == self.kandinsky_window_id))

else:
  import Xlib

  class FocusChecker:
    kandinsky_window_id = 0
    python_window_id = 0

    def __init__(self):
      if self.kandinsky_window_id == 0 and "kandinsky" in sys.modules:
        # To find kandinsky is more simple, no need to find parent processes with a valid window
        # 'TkTopLevel' is the class name of root tkinter window
        ...

        if USE_KANDINSKY_INPUT_ONLY: 
          self.python_window_id = 0
          return
        
      if self.python_window_id == 0:
        # Find python cosole window and ignore the top level of tkinter
        ...

    def __call__(self):
      # Verify is kandinsky is imported, for the first true test this will re-init the FocusChecker
      if self.kandinsky_window_id == 0 and "kandinsky" in sys.modules: self.__init__()
      
      return False

del os # no more need of this


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
