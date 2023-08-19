from .common import prettywarn
import sys, os, subprocess

# By default it just read kandinsky window (only if is focused)
USE_KANDINSKY_INPUT_ONLY = 'ION_DISABLE_KANDINSKY_INPUT_ONLY' not in os.environ
# Option to get input everywhere on system
GET_INPUT_EVERYWHERE = 'ION_ENABLE_GET_INPUT_EVERYWHERE' in os.environ


class IFocusChecker:
  """
  Base class for FocusChecker

  following methods must be redefined:
    - search_window(pid, classname, not_classname, contains_title)
    - get_focussed_window()
    - get_ppid_of_pid(pid)
  """

  kandinsky_window_id = 0
  kandinsky_not_found_error_printed = False
  python_window_id = 0
  script_pid = os.getpid()
  # used for a more specific search
  script_filename = os.path.basename(sys.argv[0])
  # 'TkTopLevel' is the class name of root tkinter window, 'pygame' because in old releases of kandinsky i used pygame
  classnames_to_search = ("TkTopLevel", "pygame")

  def __init__(self):
    if self.kandinsky_window_id == 0 and "kandinsky" in sys.modules:
      # To find kandinsky is more simple, no need to find parent processes with a valid window
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

  def search_window(self, pid=0, classname=None, not_classname=False, contains_title=None):
    raise NotImplementedError

  def _get_window(self, pid=0, classname=None, not_classname=False, contains_title=None):
    if type(pid) != int or pid < 0: raise ValueError("invalid pid")
    if not pid and not classname and not contains_title: raise ValueError("pid, classname or contains_title must be specified")
    if classname:
      if type(classname) in (list, tuple): pass
      elif type(classname) == str: classname = (classname,)
      else: raise TypeError("invalid type for classname")
    if contains_title:
      if type(contains_title) != str: raise TypeError("invalid type for contains_title")
      contains_title = contains_title.lower()

    return self.search_window(pid, classname, not_classname, contains_title)

  def get_ppid_of_pid(self, pid):
    raise NotImplementedError

  def bind_kandinsky_window(self):
    return self._get_window(self.script_pid, self.classnames_to_search, False, "kandinsky")

  def bind_python_console(self):
      wid = self._get_window(self.script_pid, self.classnames_to_search, True, self.script_filename)
      if wid == 0: wid = self._get_window(self.script_pid, self.classnames_to_search, True)

      if wid == 0:
        # Python probably started by another process, in this mode, python don't have 'real' window
        # So try going back in the parent processes to find a valid window
        ppid = os.getppid()
        for _ in range(20): # Loop limit to avoid infinite loop
          wid = self._get_window(ppid, self.classnames_to_search, True, self.script_filename)
          if wid == 0: wid = self._get_window(ppid, self.classnames_to_search, True)

          # Found an valid window
          if wid: break

          # Not found at this time, try with his ppid
          found_ppid = self.get_ppid_of_pid(ppid)
          if found_ppid < 0: continue # error happening, will try again in the next iteration
          if found_ppid == 0: break # 0 is not a valid PID (0 is the kernel itself)
          ppid = found_ppid

      return wid

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

  class FocusChecker(IFocusChecker):
    def search_window(self, pid=0, classname=None, not_classname=False, contains_title=None):
      if pid == 0: raise ValueError("a pid is needed")

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

    def get_ppid_of_pid(self, pid):
      # Use 'wmic' command to get ppid of process
      try: result = [i.strip() for i in subprocess.check_output(f"wmic process where ProcessId={pid} get ParentProcessId".split(' ')).decode().splitlines() if i.strip() != '']
      except subprocess.CalledProcessError: return -1

      if len(result) == 1: return -2
      return int(result[1].strip())

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

  class FocusChecker(IFocusChecker):
    # Use sys.argv[0] because the window classname of pygame if file name of script
    classnames_to_search = ("Tk", IFocusChecker.script_filename)

    def __init__(self):
      self.display = Xlib.display.Display()
      # Close the socket when script is finished
      atexit.register(lambda: self.display.display.close_internal("client"))
      super().__init__()

    def __del__(self):
      try: self.display.close()
      except Xlib.error.ConnectionClosedError: pass # already closed
    __exit__ = __del__

    def get_wm_pid(window):
      p = window.get_full_property(window.display.get_atom('_NET_WM_PID'), Xlib.X.AnyPropertyType)
      if p is None: return None
      return p.value[0]

    def search_window(self, pid=0, classname=None, not_classname=False, contains_title=None):
      wins = [self.display.screen().root] # should loop over all screens

      while len(wins) != 0:
        win = wins.pop(0)
        try:
          wpid = self.get_wm_pid(win)

          if (True if pid == 0 else (wpid and pid == wpid)) and win.get_attributes().map_state == Xlib.X.IsViewable:
            found = True

            if found and classname:
              wclass = win.get_wm_class()
              if not wclass or not ((not_classname and any([wclass[1] != name for name in classname])) or
                                (not not_classname and any([wclass[1] == name for name in classname]))):
                found = False

            if found and contains_title:
              wtitle = win.get_wm_name()
              # check the value because some window return an empty title with this method
              if wtitle == b'': 
                wtitle = win.get_full_property(self.display.get_atom('_NET_WM_NAME'), Xlib.X.AnyPropertyType)
                if wtitle: wtitle = wtitle.value.decode()
              if not wtitle or contains_title not in wtitle.lower(): found = False

            if found: return win.id

          subwins = win.query_tree().children
          if subwins != None: wins += subwins

        except (Xlib.error.BadWindow, TypeError): pass # catch the case of a not valid window or invalid reply
        except Xlib.error.ConnectionClosedError: break # connection closed, no need to continue to search the window
      return 0

    def bind_kandinsky_window(self):
      wid = super().bind_kandinsky_window()

      # In some linux distributions Tkinter do not set window property '_NET_WM_PID'
      # So try to find the window with a less reliable method
      # EDIT: is in all linux distributions
      if not wid: wid = self._get_window(0, self.classnames_to_search[0], False, "kandinsky")

      return wid

    def bind_python_console(self):
      # Check if is wayland because we cannot locate all windows due to security reasons
      if is_wayland and not self.kandinsky_not_found_error_printed:
        prettywarn("Wayland (used by GNOME/Ubuntu or KDE) is not fully supported. "
                   "The python console window will probably not be localized correctly. "
                   "To avoid this problem, start your session in X11 mode.", UserWarning)

      return super().bind_python_console()

    def get_ppid_of_pid(self, pid):
      try: result = subprocess.check_output(f"ps -o ppid= {pid}".split(' ')).decode().strip()
      except subprocess.CalledProcessError: return -1
      
      # check the return value
      if not result: return -2
      return int(result)

    def get_focussed_window(self):
      # remove the resource warning
      if ("ignore", None, ResourceWarning, None, 0) not in warnings.filters: warnings.simplefilter("ignore", ResourceWarning)
      return self.display.screen().root.get_full_property(self.display.get_atom('_NET_ACTIVE_WINDOW'), Xlib.X.AnyPropertyType).value[0]


elif sys.platform.startswith("darwin"):
  try:
    from AppKit import NSWorkspace
    from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID
  except ImportError as e:
    e.msg = "pyobjc module and the Quartz extension are not installed. Please install it with command 'pip install pyobjc-core pyobjc-framework-Quartz'"
    raise

  class FocusChecker(IFocusChecker):
    #classnames_to_search = ("", "")

    def search_window(self, pid=0, classname=None, not_classname=False, contains_title=None):
      for win in CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID):
        if pid == 0 or win['kCGWindowOwnerPID'] == pid:
          if classname:
            windowClassName = ... #TODO: find the classname
            if not ((not_classname and any([windowClassName != name for name in classname])) or
                (not not_classname and any([windowClassName == name for name in classname]))):
              continue

          if contains_title:
            windowTitle = win.get('kCGWindowName', None)
            if not windowTitle or contains_title not in windowTitle.lower(): continue

          return win['kCGWindowNumber']
      return 0

    def get_ppid_of_pid(self, pid):
      try: result = subprocess.check_output(f"ps -o ppid= {pid}".split(' ')).decode().strip()
      except subprocess.CalledProcessError: return -1
      
      # check the return value
      if not result: return -2
      return int(result)

    def get_focussed_window(self):
      front_app_pid = NSWorkspace.sharedWorkspace().frontmostApplication().processIdentifier()
      for win in CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID):
        if win['kCGWindowOwnerPID'] == front_app_pid:
          return win['kCGWindowNumber']
      return 0 # cannot happening


else:
  # Platform not supported for focus, create an fake FocusChecker class
  # The 'focus on only window' will be disabled
  prettywarn(f"platform '{sys.platform}' not supported for inputs only in focussed window. "
              "Inputs will be gets on entire system", ImportWarning)
  FocusChecker = NoopFocusChecker
