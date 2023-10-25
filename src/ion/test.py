import os
#os.environ['ION_ENABLE_DEBUG'] = ''
os.environ['ION_OS_MODE'] = '3'
from __init__ import *
from kandinsky import *

while 1:
  k = get_keys()
  if k: print(k)
  #display(True)
