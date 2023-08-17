from .common import prettywarn
import sys, os, subprocess

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

      if self.python_window_id == 0:
        # No valid (parent) window found!
        # Python probably started in no-shell-mode and/or by a task
        # So will not log python console inputs
        prettywarn("cannot find an valid window to get inputs from python console.", RuntimeWarning)

  def __call__(self):
    # Verify is kandinsky is imported, for the first true test (if no error) this will re-init FocusChecker
    if self.kandinsky_window_id == 0 and "kandinsky" in sys.modules: self.__init__()

    focussed = self.get_focussed_window()
    return ((self.python_window_id and focussed == self.python_window_id) or
            (self.kandinsky_window_id and focussed == self.kandinsky_window_id))

  def bind_kandinsky_window(self):
    raise NotImplementedError

  def bind_python_console(self):
    raise NotImplementedError

  def get_focussed_window(self):
    raise NotImplementedError

# Fake FocusChecker class, will always return True
class NoopFocusChecker(IFocusChecker):
  def __init__(self): return
  def __call__(self): return True



if GET_INPUT_EVERYWHERE:
  FocusChecker = NoopFocusChecker


elif sys.platform.startswith("win"):
  import ctypes

  def GetFirstWindowFromThreadProcessId(pid, classname=None, not_classname=False, contains_title=None):
    if classname:
      if type(classname) in (list, tuple): pass
      elif type(classname) == str: classname = (classname,)
      else: raise TypeError("invalid type for class name")
    if contains_title:
      if type(contains_title) != str: raise TypeError("invalid type for contains name")
      contains_title = contains_title.lower()

    def foreach_window(hwnd, _):
      lpdw = ctypes.c_uint()
      ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(lpdw))

      if lpdw.value == pid and ctypes.windll.user32.IsWindowVisible(hwnd):
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

  class FocusChecker(IFocusChecker):
    def bind_kandinsky_window(self):
      return GetFirstWindowFromThreadProcessId(os.getpid(), ("TkTopLevel", "pygame"), False, "kandinsky")

    def bind_python_console(self):
      # First, try to search the script name in title of window, for a more specific search
      main_script = os.path.basename(sys.argv[0])

      wid = GetFirstWindowFromThreadProcessId(os.getpid(), ("TkTopLevel", "pygame"), True, main_script)
      if wid == 0: wid = GetFirstWindowFromThreadProcessId(os.getpid(), ("TkTopLevel", "pygame"), True)

      if wid == 0:
        # Python probably started by another process, in this mode, python don't have 'real' window
        # So try going back in the parent processes to find a valid window
        ppid = os.getppid()
        for _ in range(20): # Loop limit to avoid infinite loop
          wid = GetFirstWindowFromThreadProcessId(ppid, ("TkTopLevel", "pygame"), True, main_script)
          if wid == 0: wid = GetFirstWindowFromThreadProcessId(ppid, ("TkTopLevel", "pygame"), True)

          # Found an valid window
          if wid: break

          # Not found at this time, try with his ppid
          # Use 'wmic' command to get ppid of process
          try: result = [i.strip() for i in subprocess.check_output(f"wmic process where ProcessId={ppid} get ParentProcessId".split(' ')).decode().splitlines() if i.strip() != '']
          except subprocess.CalledProcessError: continue # Error happening, will try again in the next iteration

          if len(result) == 1:
            # No parent found, parent died or idk
            del check_output, CalledProcessError
            break
          else: ppid = int(result[1].strip())

      return wid

    def get_focussed_window(self):
      return ctypes.windll.user32.GetForegroundWindow()


elif sys.platform.startswith("linux"):
  try: import Xlib
  except ImportError as e:
    e.msg = "Xlib module not installed. Please install it with command 'pip install python-xlib'"
    raise
  import atexit, warnings

  # Check graphical server type
  try: graphical_server_type = subprocess.check_output("loginctl show-session $(loginctl | awk '/'$(whoami)'/ {print $1}') -p Type | awk -F = '{print $2}'", shell=True, stderr=subprocess.STDOUT).decode().strip()
  except subprocess.CalledProcessError as e:
    if "not been booted" in e.stdout.decode().strip(): # propably a non graphical system or no login manager
      prettywarn("no graphical server instance detected, falling back to x11 support", RuntimeWarning)   
    else: prettywarn("failed to get graphical server type, falling back to x11 support", RuntimeWarning)
    # Fall baack to x11 support
    graphical_server_type = "x11"
  else:
    if "not been booted" in graphical_server_type:
      prettywarn("no graphical server instance detected, falling back to x11 support", RuntimeWarning)   
      graphical_server_type = "x11"

    # x11 or wayland, or... other? can be?
    if graphical_server_type not in ("x11", "wayland"):
      prettywarn(f"graphical server {graphical_server_type!r} not supported, falling back to x11 support", RuntimeWarning)
  
  # TODO: complete support of wayland
  is_wayland = graphical_server_type == "wayland"

  def get_wm_pid(window):
    p = window.get_full_property(window.display.get_atom('_NET_WM_PID'), Xlib.X.AnyPropertyType)
    if p is None: return None
    return p.value[0]

  def search_window(display, pid=0, classname=None, not_classname=False, contains_title=None):
    if type(pid) != int or pid < 0: raise ValueError("invalid pid")
    if not pid and not classname and not contains_title: raise ValueError("pid, classname or contains_title must be specified")
    if classname:
      if type(classname) in (list, tuple): pass
      elif type(classname) == str: classname = (classname,)
      else: raise TypeError("invalid type for classname")
    if contains_title:
      if type(contains_title) != str: raise TypeError("invalid type for contains_title")
      contains_title = contains_title.lower()

    wins = [display.screen().root] # should loop over all screens

    while len(wins) != 0:
        win = wins.pop(0)
        try:
          wpid = get_wm_pid(win)

          if (True if pid == 0 else (wpid and pid == wpid)) and win.get_attributes().map_state == Xlib.X.IsViewable:
            found = True

            if found and classname:
              wclass = win.get_wm_class()
              if not wclass or not ((not_classname and any([wclass[1] != name for name in classname])) or
                  (not not_classname and any([wclass[1] == name for name in classname]))):
                found = False

            if found and contains_title:
              wtitle = win.get_wm_name()
              if not wtitle or contains_title not in wtitle.lower(): found = False

            if found: return win.id

        except Xlib.error.BadWindow: pass # catch the case of a not valid window (sometimes apear on Wayland)

        subwins = win.query_tree().children
        if subwins != None: wins += subwins

    return 0


  class FocusChecker(IFocusChecker):
    def __init__(self):
      self.display = Xlib.display.Display()
      # Close the socket when script is finished
      atexit.register(lambda: self.display.display.close_internal("client"))
      super().__init__()

    def __del__(self):
      try: self.display.close()
      except Xlib.error.ConnectionClosedError: pass # already closed
    __exit__ = __del__

    def bind_kandinsky_window(self):
      # Use sys.argv[0] because the window classname of pygame if file name of script
      wid = search_window(self.display, os.getpid(), ("Tk", os.path.basename(sys.argv[0])), False, "kandinsky")
      # In some linux distributions Tkinter do not set window property '_NET_WM_PID'
      # So try to find the window with a less reliable method
      # EDIT: is in all linux distributions
      if not wid: wid = search_window(self.display, 0, "Tk", False, "kandinsky")
      return wid

    def bind_python_console(self):
      # Check if is wayland because we cannot locate all windows due to security reasons
      if is_wayland:
        prettywarn("Wayland (used by GNOME/Ubuntu or KDE) is not fully supported. "
                   "The python console window will probably not be localized correctly. "
                   "To avoid this problem, start your session in X11 mode.", UserWarning)

      # First, try to search the script name in title of window, for a more specific search
      main_script = os.path.basename(sys.argv[0])

      wid = search_window(self.display, os.getpid(), ("Tk", main_script), True, main_script)
      if wid == 0: wid = search_window(self.display, os.getpid(), ("Tk", main_script), True)

      if wid == 0:
        # Python probably started by another process, in this mode, python don't have 'real' window
        # So try going back in the parent processes to find a valid window
        ppid = os.getppid()
        for _ in range(20): # Loop limit to avoid infinite loop
          wid = search_window(self.display, ppid, ("Tk", main_script), True, main_script)
          if wid == 0: wid = search_window(self.display, ppid, ("Tk", main_script), True)

          # Found an valid window
          if wid: break

          # Not found at this time, try with his ppid
          try: result = subprocess.check_output(f"ps -o ppid= {ppid}".split(' ')).decode().strip()
          except subprocess.CalledProcessError: continue # Error happening, will try again in the next iteration

          if not result: break
          else: ppid = int(result)
          if not ppid: break

      return wid

    def get_focussed_window(self):
      # remove the resource warning
      if ("ignore", None, ResourceWarning, None, 0) not in warnings.filters: warnings.simplefilter("ignore", ResourceWarning)
      return self.display.screen().root.get_full_property(self.display.get_atom('_NET_ACTIVE_WINDOW'), 0).value[0]


elif sys.platform.startswith("darwin"):

  class FocusChecker(IFocusChecker):
    def bind_kandinsky_window(self):
      ...

    def bind_python_console(self):
      ...

    def get_focussed_window(self):
      ...


else:
  # Platform not supported for focus, create an fake FocusChecker class
  # The 'focus on only window' will be disabled
  prettywarn(f"platform '{sys.platform}' not supported for inputs only in focussed window. "
              "Inputs will be gets on entire system", ImportWarning)
  FocusChecker = NoopFocusChecker
