from .common import prettywarn
import sys, os

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
        prettywarn("could not find the kandinsky window to get inputs.", RuntimeWarning)
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


if GET_INPUT_EVERYWHERE:
  # Fake FocusChecker class, will always return True
  class FocusChecker:
    def __call__(self): return True


elif sys.platform.startswith("win"):
  import ctypes

  def GetFirstWindowFromThreadProcessId(pid, class_name=None, not_class_name=False, contains_name=None):
    window = ctypes.c_uint(0)
    if class_name:
      if type(class_name) in (list, tuple): pass
      elif type(class_name) == str: class_name = (class_name,)
      else: raise TypeError("invalid type for class name")
    if contains_name and type(contains_name) != str: raise TypeError("invalid type for contains name")
    
    def foreach_window(hwnd, _):
      lpdw = ctypes.c_uint()
      ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(lpdw))
      
      if lpdw.value == pid and ctypes.windll.user32.IsWindowVisible(hwnd):
        if class_name:
          buff = ctypes.create_unicode_buffer(256)
          ctypes.windll.user32.GetClassNameW(hwnd, buff)
 
          if not ((not_class_name and any([buff.value != name for name in class_name])) or
                  (not not_class_name and any([buff.value == name for name in class_name]))): 
            return True
        
        if contains_name:
          buff = ctypes.create_unicode_buffer(256)
          ctypes.windll.user32.GetWindowTextW(hwnd, buff, 256)

          if contains_name.lower() not in buff.value.lower(): return True
             
        window.value = hwnd
        return False
      return True
    
    ctypes.windll.user32.EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_uint, ctypes.c_uint)(foreach_window), 0)
    return window.value

  class FocusChecker(IFocusChecker):
    def bind_kandinsky_window(self):
      return GetFirstWindowFromThreadProcessId(os.getpid(), ("TkTopLevel", "pygame"), False, "kandinsky")
    
    def bind_python_console(self):
      wid = GetFirstWindowFromThreadProcessId(os.getpid(), ("TkTopLevel", "pygame"), True)

      if wid == 0:
        # Python probably started by another process, in this mode, python don't have 'real' window
        # So try going back in the parent processes to find a valid window
        ppid = os.getppid()
        for _ in range(20): # Loop limit to avoid infinite loop
          wid = GetFirstWindowFromThreadProcessId(ppid, ("TkTopLevel", "pygame"), True)

          # Found an valid window
          if wid: break

          # Not found at this time, try with his ppid
          from subprocess import check_output, CalledProcessError # need this because calling 'wmic' directly
          try: result = [i.strip() for i in check_output(["wmic", "process", "where", f"ProcessId={ppid}", "get", "ParentProcessId"]).decode().splitlines() if i.strip() != '']
          except CalledProcessError: continue # Error happening, will try again in the next iteration

          if len(result) == 1:
            # No parent found, parent died or idk
            prettywarn("cannot find an valid window to get inputs from python console.", RuntimeWarning)
            del check_output, CalledProcessError
            break
          else: ppid = int(result[1].strip())

        else: 
          # No valid parent window found!
          # Python probably started in no-shell-mode and/or by a task
          # So will not log python console inputs
          prettywarn("cannot find an valid window to get inputs from python console.", RuntimeWarning)

      return wid
    
    def check_console_focus(self):
      return ctypes.windll.user32.GetForegroundWindow() == self.python_window_id
    
    def check_kandinsky_focus(self):
      return ctypes.windll.user32.GetForegroundWindow() == self.kandinsky_window_id
  

elif sys.platform.startswith("linux"):
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


elif sys.platform.startswith("darwin"):

  class FocusChecker(IFocusChecker):
    def bind_kandinsky_window(self):
      ...
  
    def bind_python_console(self):
      ...

    def check_kandinsky_focus(self):
      ...
      
    def check_console_focus(self):
      ...

else:
  # Platform not supported for focus, create an fake FocusChecker class
  # The 'focus on only window' will be disabled
  prettywarn(f"platform '{sys.platform}' not supported for inputs only in focussed window. "
              "Inputs will be gets on entire system", ImportWarning)

  class FocusChecker:
    def __call__(self): return True