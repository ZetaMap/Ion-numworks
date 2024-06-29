from ..common import prettywarn, print_debug
import sys, os

# By default it just read kandinsky window (only if is focused)
DISABLE_KANDINSKY_INPUT_ONLY = 'ION_DISABLE_KANDINSKY_INPUT_ONLY' in os.environ
# Option to get input everywhere on system
GET_INPUT_EVERYWHERE = 'ION_ENABLE_GET_INPUT_EVERYWHERE' in os.environ


class BaseFocusChecker:
  """
  Base class for FocusChecker

  following methods must be overrided:
    - check_window(wid, pid, classname, not_classname, contains_title)
    - search_window(pid, classname, not_classname, contains_title)
    - get_focussed_window()
    - get_ppid_of_pid(pid)
  """

  kandinsky_window_id = 0
  kandinsky_not_found_error_printed = False
  python_window_id = 0
  python_not_found_error_printed = False
  script_pid = os.getpid()
  # used for a more specific search
  script_filename = os.path.basename(sys.argv[0])
  
  # must contains this name
  winname = "kandinsky"
  # 'TkTopLevel' is the class name of root tkinter window, 'pygame' because in old releases of kandinsky i used pygame
  classnames = ("TkTopLevel", "pygame")

  def __init__(self):
    self.bind_windows()
    self.register_window_callbacks()

  def __call__(self, just_check=False):
    # check if windows still exists, to stop the KeyLogger properly
    self.check_windows_availability()
    if just_check: return False
    
    self.bind_windows()
    focussed = self.get_focussed_window()

    return ((self.python_window_id and focussed == self.python_window_id) or
            (self.kandinsky_window_id and focussed == self.kandinsky_window_id))

  def bind_windows(self):
    if (DISABLE_KANDINSKY_INPUT_ONLY or self.kandinsky_window_id == 0) and self.python_window_id == 0:
      # Find python console window and ignore the top level of tkinter
      self.python_window_id = self.get_python_console_window()

      if self.python_window_id == 0:
        # No valid (parent) window found!
        # Python probably started in no-shell-mode and/or by a task
        # So will not log python console inputs
        if not self.python_not_found_error_printed:
          prettywarn("unable to find an valid window to get inputs from python console.", RuntimeWarning)
          self.python_not_found_error_printed = True
      else: print_debug("FocusChecker", f"found the window '{self.python_window_id}' as python console")
    
    # Verify is kandinsky is imported
    if self.kandinsky_window_id == 0 and "kandinsky" in sys.modules:
      # To find kandinsky is more simple, no need to find parent processes with a valid window
      self.kandinsky_window_id = self.get_kandinsky_window()

      if self.kandinsky_window_id == 0:
        # Kandinsky window not found
        if not self.kandinsky_not_found_error_printed:
          prettywarn("could not find the kandinsky window to get inputs.", RuntimeWarning)
          self.kandinsky_not_found_error_printed = True
      else: print_debug("FocusChecker", f"found the window '{self.kandinsky_window_id}' as kandinsky")

    if self.kandinsky_window_id and not DISABLE_KANDINSKY_INPUT_ONLY:
      self.python_window_id = 0

  def check_windows_availability(self):
    if self.kandinsky_window_id == -1:
      raise RuntimeError(f"Kandinsky window destroyed. Unable to locate it.")
    if self.python_window_id == -1:
      raise RuntimeError(f"Python console window destroyed. Unable to locate it.")

  def check_window(self, wid, pid=0, classname=None, not_classname=False, contains_title=None):
    raise NotImplementedError

  def search_window(self, pid=0, classname=None, not_classname=False, contains_title=None):
    raise NotImplementedError

  def get_window(self, pid=0, classname=None, not_classname=False, contains_title=None, wid=0):
    if type(wid) != int: raise ValueError("invalid wid")
    if type(pid) != int or pid < 0: raise ValueError("invalid pid")
    if not pid and not classname and not contains_title: raise ValueError("pid, classname or contains_title must be specified")
    if classname:
      if type(classname) in (list, tuple): pass
      elif type(classname) == str: classname = (classname,)
      else: raise TypeError("invalid type for classname")
    if contains_title:
      if type(contains_title) != str: raise TypeError("invalid type for contains_title")
      contains_title = contains_title.lower()

    if wid == 0: return self.search_window(pid, classname, not_classname, contains_title)
    return wid if self.check_window(wid, pid, classname, not_classname, contains_title) else 0

  def get_ppid(self, pid):
    raise NotImplementedError

  def get_kandinsky_window(self, wid=0):
    return self.get_window(self.script_pid, self.classnames, False, self.winname, wid)

  def get_python_console_window(self, wid=0):
      wid = self.get_window(self.script_pid, self.classnames, True, self.script_filename, wid)
      if wid == 0: wid = self.get_window(self.script_pid, self.classnames, True, wid=wid)

      if wid == 0:
        # Python probably started by another process, in this mode, python don't have 'real' window
        # So try going back in the parent processes to find a valid window
        ppid = os.getppid()
        for _ in range(20): # Loop limit to avoid infinite loop
          wid = self.get_window(ppid, self.classnames, True, self.script_filename, wid)
          if wid == 0: wid = self.get_window(ppid, self.classnames, True, wid=wid)

          # Found an valid window
          if wid: break

          # Not found at this time, try with his ppid
          found_ppid = self.get_ppid(ppid)
          if found_ppid < 0: continue # error happening, will try again in the next iteration
          if found_ppid == 0: break # 0 is not a valid PID (0 is the kernel itself)
          ppid = found_ppid

      return wid

  def get_focussed_window(self):
    raise NotImplementedError

  def register_window_callbacks(self):
    return


# Fake FocusChecker class, will always return True
class NoopFocusChecker(BaseFocusChecker):
  def __init__(self): return
  def __call__(self, just_check=False): return True
