from .base import *
from threading import Thread

import signal, warnings, subprocess

try:
  import Xlib
  import Xlib.xobject.drawable
except ImportError as e:
  e.msg = "Xlib module not installed. Please install it with command 'pip install python-xlib'"
  raise


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

# remove the resource warning
if ("ignore", None, ResourceWarning, None, 0) not in warnings.filters: 
  warnings.simplefilter("ignore", ResourceWarning)


class FocusChecker(BaseFocusChecker):
  # Use sys.argv[0] because the window classname of pygame if file name of script
  classnames = ("Tk", BaseFocusChecker.script_filename)

  def __init__(self):
    self.display = Xlib.display.Display()
    # Close the socket when script is finished
    signal.signal(signal.SIGINT|signal.SIGTERM|signal.SIGKILL|signal.SIGQUIT,
                  lambda: self.display.display.close_internal("client"))
    super().__init__()

  def __del__(self):
    try: self.display.close()
    except Xlib.error.ConnectionClosedError: pass # already closed
  __exit__ = __del__

  def get_wm_pid(self, window):
    p = window.get_full_property(window.display.get_atom('_NET_WM_PID'), Xlib.X.AnyPropertyType)
    if p is None: return None
    return p.value[0]

  def check_window(self, wid, pid=0, classname=None, not_classname=False, contains_title=None):
    # get the window object by his id
    if isinstance(wid, Xlib.xobject.drawable.Window): win = wid
    else: win = self.display.create_resource_object('window', wid)

    wpid = self.get_wm_pid(win)
    found = False

    if (pid == 0 or (wpid and pid == wpid)) and win.get_attributes().map_state == Xlib.X.IsViewable:
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

    return found

  def search_window(self, pid=0, classname=None, not_classname=False, contains_title=None):
    wins = [self.display.screen().root] # should loop over all screens

    while len(wins) != 0:
      win = wins.pop(0)
      try:
        if self.check_window(win, pid, classname, not_classname, contains_title): return win.id

        subwins = win.query_tree().children
        if subwins != None: wins += subwins

      except (Xlib.error.BadWindow, TypeError): pass # catch the case of a not valid window or invalid reply
      except Xlib.error.ConnectionClosedError: break # connection closed, no need to continue to search the window
    return 0

  def register_window_callbacks(self):
    def event_loop():
      # grab events
      self.display.screen().root.change_attributes(event_mask=Xlib.X.SubstructureNotifyMask)

      search_windows = True
      event = None
      
      while (self.kandinsky_window_id != -1 or
            (DISABLE_KANDINSKY_INPUT_ONLY and self.python_window_id != -1)):
        event = self.display.next_event()

        if event.type == Xlib.X.DestroyNotify:
          wid = event.window.id + 1 # idk why, i never the exact window id
          if wid == self.kandinsky_window_id: self.kandinsky_window_id = -1
          elif wid == self.python_window_id: self.python_window_id = -1

        if search_windows:
          self.bind_windows()
          if self.kandinsky_window_id and self.python_window_id: search_windows = False

    self.thread = Thread(name="WindowDestroyDetector", target=event_loop, daemon=True)
    self.thread.start()

  def get_kandinsky_window(self, wid=0):
    wid = super().get_kandinsky_window(wid)

    # In some linux distributions, Tkinter do not set window property '_NET_WM_PID'.
    # So try to find the window with a less reliable method.
    # EDIT: is in all linux distributions
    # EDIT2: Fixed in version 2.7.1 of kandinsky
    if not wid: wid = self.get_window(0, self.classnames[0], False, self.winname, wid)

    return wid

  def get_python_console_window(self, wid=0):
    # Check if is wayland because we cannot locate all windows due to "security reasons"
    if is_wayland and not self.kandinsky_not_found_error_printed:
      prettywarn("Wayland (used by GNOME, Ubuntu or KDE) is not fully supported. "
                  "The python console window will probably not be localized correctly. "
                  "To avoid this problem, start your session in X11 mode.", UserWarning)

    return super().get_python_console_window(wid)

  def get_ppid(self, pid):
    try: result = subprocess.check_output(f"ps -o ppid= {pid}".split(' ')).decode().strip()
    except subprocess.CalledProcessError: return -1

    # check the return value
    if not result: return -2
    try: return int(result)
    except ValueError: return -3

  def get_focussed_window(self):
    return self.display.screen().root.get_full_property(self.display.get_atom('_NET_ACTIVE_WINDOW'), Xlib.X.AnyPropertyType).value[0]
