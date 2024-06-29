"""
Source: https://github.com/smokris/GetWindowID
Converted in Python by CodeConvert.ai
And modified for my own use
"""

import sys
if not sys.platform.startswith("darwin"):
  file_name = __file__[__file__.rfind("/")+1 or __file__.rfind("\\")+1:]
  raise ImportError(file_name + " can only be used on MacOS")
del sys

import Quartz


def search_window_id(requested_app, requested_window="", ignore_requested_app=False):
  session = Quartz.CGSessionCopyCurrentDictionary()
  if session: session.release()

  for window in Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListExcludeDesktopElements, Quartz.kCGNullWindowID):
    wid = get_window_id(window, requested_app, requested_window, ignore_requested_app)
    if wid != 0:
      return wid
  return 0

def get_window_id(window, requested_app, requested_window="", ignore_requested_app=False):
  """Return 0 if window is not the right, else his window id"""
  app = window.get("kCGWindowOwnerName", None)
  window_title = window.get("kCGWindowName", "") or window.get("kCGWindowTitle", "")
  bounds = window["kCGWindowBounds"]

  if (app != requested_app if ignore_requested_app else app == requested_app):
    aspect = bounds["Width"] / bounds["Height"]
    if aspect > 30:
      # If it's that wide and short, it's probably the system menu bar, so ignore it.
      return 0

    if requested_window:
      if not window_title:
        # If CGWindowListCopyWindowInfo didn't give us the window title, try to extract it from the Accessibility API.
        window_title = get_window_title_from_accessibility(window)

      if (window_title != requested_window or
          (window_title == "Focus Proxy" 
           and bounds["Width"] == 1 and bounds["Height"] == 1)):
        return 0
    return window["kCGWindowNumber"]
  return 0

def get_window_title_from_accessibility(window):
  ax_app = Quartz.AXUIElementCreateApplication(window["kCGWindowOwnerPID"])
  windows = Quartz.AXUIElementCopyAttributeValue(ax_app, Quartz.kAXWindowsAttribute)

  if windows == Quartz.kAXErrorSuccess:
    for ax_window in windows:
      # The Accessibility API doesn't expose a unique identifier for the window, so guess based on its frame.
      position = Quartz.AXUIElementCopyAttributeValue(ax_window, Quartz.kAXPositionAttribute)
      size = Quartz.AXUIElementCopyAttributeValue(ax_window, Quartz.kAXSizeAttribute)
      bounds = window["kCGWindowBounds"]

      if position == Quartz.kAXErrorSuccess and size == Quartz.kAXErrorSuccess:
        ax_position = Quartz.AXValueGetValue(position, Quartz.kAXValueTypeCGPoint)
        ax_size = Quartz.AXValueGetValue(size, Quartz.kAXValueTypeCGSize)

        if (ax_position.x == bounds.origin.x and ax_position.y == bounds.origin.y and
            ax_size.width == bounds.size.width and ax_size.height == bounds.size.height):
          return Quartz.AXUIElementCopyAttributeValue(ax_window, Quartz.kAXTitleAttribute)

  return ""
