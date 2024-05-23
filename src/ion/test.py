import os, time
#os.environ['ION_DISABLE_KANDINSKY_INPUT_ONLY'] = ''
#os.environ['ION_GET_INPUT_EVERYWHERE'] = ''
os.environ['ION_OS_MODE'] = '3'
from __init__ import *
from kandinsky import *

while 1:
  k = get_keys()
  if k: print(k)
  if "alpha" in k: 
    from kandinsky import *
  #display(True)
  time.sleep(0.01)
