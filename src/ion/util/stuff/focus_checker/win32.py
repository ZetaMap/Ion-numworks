from .base import *
from threading import Thread

import ctypes, ctypes.wintypes, time, subprocess

class FocusChecker(BaseFocusChecker):
  def check_window(self, wid, pid=0, classname=None, not_classname=False, contains_title=None):
    if pid == 0: raise ValueError("a pid is needed")

    lpdw = ctypes.c_uint()
    ctypes.windll.user32.GetWindowThreadProcessId(wid, ctypes.byref(lpdw))

    if lpdw.value == pid and ctypes.windll.user32.IsWindowVisible(wid):
      if classname:
        buff = ctypes.create_unicode_buffer(256)
        ctypes.windll.user32.GetClassNameW(wid, buff)

        if not ((not_classname and any([buff.value != name for name in classname])) or
            (not not_classname and any([buff.value == name for name in classname]))):
          return False

      if contains_title:
        buff = ctypes.create_unicode_buffer(256)
        ctypes.windll.user32.GetWindowTextW(wid, buff, 256)

        if contains_title not in buff.value.lower(): 
          return False
      return True
    return False

  def search_window(self, pid=0, classname=None, not_classname=False, contains_title=None):
    if pid == 0: raise ValueError("a pid is needed")

    def foreach_window(hwnd, _):
      if self.check_window(hwnd, pid, classname, not_classname, contains_title):
        window.value = hwnd
        return False
      return True

    window = ctypes.c_uint(0)
    ctypes.windll.user32.EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_uint, ctypes.c_uint)(foreach_window), 0)
    return window.value

  def register_window_callbacks(self):
    def window_state(hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
      if idChild == idObject:
        if hwnd == self.kandinsky_window_id: self.kandinsky_window_id = -1
        elif hwnd == self.python_window_id: self.python_window_id = -1

    def register_hook():
      hook = ctypes.WINFUNCTYPE(
        ctypes.wintypes.HANDLE,
        ctypes.wintypes.HANDLE,
        ctypes.wintypes.DWORD,
        ctypes.wintypes.HWND,
        ctypes.wintypes.LONG,
        ctypes.wintypes.LONG,
        ctypes.wintypes.DWORD,
        ctypes.wintypes.DWORD
      )(window_state)
      search_windows = True
      hook_id = ctypes.windll.user32.SetWinEventHook(0x8001, 0x8001, None, hook, 0, 0, 0)

      if hook_id:
        msg = ctypes.wintypes.MSG()
        while (self.kandinsky_window_id != -1 or 
                (DISABLE_KANDINSKY_INPUT_ONLY and self.python_window_id != -1)):
          time.sleep(0.1)
          r = ctypes.windll.user32.PeekMessageW(ctypes.byref(msg), None, 0, 0, 0)

          if r == 0:
            ctypes.windll.user32.TranslateMessage(msg)
            ctypes.windll.user32.DispatchMessageW(msg)
          elif r <=0 or msg.message == 0x0401: 
            prettywarn("window destroy detector has been broken", RuntimeWarning)
            break

          if search_windows:
            self.bind_windows()
            if self.kandinsky_window_id and self.python_window_id: search_windows = False

        ctypes.windll.user32.UnhookWinEvent(hook_id)
      else: prettywarn("cannot hook the window destroy detector", RuntimeWarning)


    self.thread = Thread(name="WindowDestroyDetector", target=register_hook, daemon=True)
    self.thread.start()

  def get_ppid(self, pid):
    # TODO: idk how to get this information better than that
    # Use 'wmic' command to get ppid of process
    try: result = [i.strip() for i in subprocess.check_output(f"wmic process where ProcessId={pid} get ParentProcessId".split(' '), stderr=subprocess.PIPE).decode().splitlines() if i.strip() != '']
    except subprocess.CalledProcessError: return -1

    if len(result) < 2: return -2
    return int(result[1].strip())

  def get_focussed_window(self):
    return ctypes.windll.user32.GetForegroundWindow()
