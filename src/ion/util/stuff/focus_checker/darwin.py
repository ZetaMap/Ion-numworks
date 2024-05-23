from .base import *

import subprocess

try:
  from AppKit import NSWorkspace
  from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID
except ImportError as e:
  e.msg = "pyobjc module and the Quartz extension are not installed. Please install it with command 'pip install pyobjc-core pyobjc-framework-Quartz'"
  raise


class FocusChecker(BaseFocusChecker):
  classnames_to_search = ("Tk", "pygame")
  #CGWindowListCreateDescriptionFromArray
  def search_window(self, pid=0, classname=None, not_classname=False, contains_title=None):
    for win in CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID):
      if pid == 0 or win['kCGWindowOwnerPID'] == pid:
        if classname:
          windowClassName = ... #TODO: find the classname
          if not ((not_classname and any([windowClassName != name for name in classname])) or
              (not not_classname and any([windowClassName == name for name in classname]))):
            continue

        if contains_title:
          windowTitle = win.get('kCGWindowName', None) or win.get('kCGWindowTitle', None)
          if not windowTitle or contains_title not in windowTitle.lower(): continue

        return win['kCGWindowNumber']
    return 0

  def get_ppid(self, pid):
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
