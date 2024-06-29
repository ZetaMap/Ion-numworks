from .base import *
from threading import Thread

import subprocess

try:
  from AppKit import NSWorkspace
  from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID
  from .darwin_GetWindowID import get_window_id
except ImportError as e:
  e.msg = ("pyobjc module and/or the Quartz extension are not installed. \n"
           "Please install them with command: pip install pyobjc-core pyobjc-framework-Quartz")
  raise


class FocusChecker(BaseFocusChecker):
  #classnames is the window owner
  classnames = ("Python",)
  #CGWindowListCreateDescriptionFromArray
  
  def check_window(self, wid, pid=0, classname=None, not_classname=False, contains_title=None):
    # get window object
    win = ...
    
    if pid == 0 or win['kCGWindowOwnerPID'] == pid:
      if classname: 
        return get_window_id(win, classname[0], not_classname, contains_title) != 0
      return True
    return False
  
  def search_window(self, pid=0, classname=None, not_classname=False, contains_title=None):
                                        # kCGWindowListExcludeDesktopElements
    for win in CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID):
      if self.check_window(win, pid, classname, not_classname, contains_title):
        return win['kCGWindowNumber']
    return 0

  def register_window_callbacks(self):
    ...

  def get_ppid(self, pid):
    try: result = subprocess.check_output(f"ps -o ppid= {pid}".split(' ')).decode().strip()
    except subprocess.CalledProcessError: return -1

    # check the return value
    if not result: return -2
    return int(result)

  def get_focussed_window(self):
    front_app_pid = NSWorkspace.sharedWorkspace().frontmostApplication().processIdentifier()
    return self.search_window(front_app_pid) # 0 cannot happening
