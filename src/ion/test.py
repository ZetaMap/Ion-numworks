#import ctypes, ctypes.wintypes, time
#
#class test:
#  def __init__(self):
#    self.kandinsky_window_id = ctypes.windll.user32.GetForegroundWindow()
#
#    def window_state(hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
#      if hwnd == self.kandinsky_window_id:
#        print("kandinsky window destroyed!")
#        ctypes.windll.user32.PostThreadMessageW(ctypes.windll.kernel32.GetCurrentThreadId(), 0x0401, 0, 0)
#        self.kandinsky_window_id = -1
#      
#    
#    hook = ctypes.WINFUNCTYPE(
#      ctypes.wintypes.HANDLE, 
#      ctypes.wintypes.HANDLE,
#      ctypes.wintypes.DWORD,
#      ctypes.wintypes.HWND,
#      ctypes.wintypes.LONG,
#      ctypes.wintypes.LONG,
#      ctypes.wintypes.DWORD,
#      ctypes.wintypes.DWORD
#    )(window_state)
#
#    hooked = ctypes.windll.user32.SetWinEventHook(0x8001, 0x8001, None, hook, 0, 0, 0)
#
#    if hooked:
#      msg = ctypes.wintypes.MSG()
#      while self.kandinsky_window_id != -1:
#        r = ctypes.windll.user32.PeekMessageW(ctypes.byref(msg), None, 0, 0, 0)
#        print(r)
#        if r == 0: 
#          ctypes.windll.user32.TranslateMessage(msg)
#          ctypes.windll.user32.DispatchMessageW(msg)
#        elif r <=0 or msg.message == 0x0401: break
#        time.sleep(0.01)
#      ctypes.windll.user32.UnhookWinEvent(hook)
#    else: print("cannot hook the window destroy detector", RuntimeWarning)
#
#
#time.sleep(5)
#print("time")
#test()
#
#exit()

import os, time
os.environ['ION_DISABLE_KANDINSKY_INPUT_ONLY'] = ''
os.environ['ION_OS_MODE'] = '3'
from __init__ import *
from kandinsky import *

while 1:
  k = get_keys()
  if k: print(k)
  #display(True)
  time.sleep(0.01)
