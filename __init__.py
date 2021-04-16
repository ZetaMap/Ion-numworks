"""
This is the adaptation of Ion module of Numworks.
Please don't use keyboard and this module at the same time.
"""
### v All keys of Numworks v ###
KEY_LEFT=0
KEY_UP=1
KEY_DOWN=2
KEY_RIGHT=3
KEY_OK=4
KEY_BACK=5
KEY_HOME=6
KEY_ONOFF=7
KEY_SHIFT=8
KEY_ALPHA=9
KEY_XNT=10
KEY_VAR=11
KEY_TOOLBOX=12
KEY_BACKSPACE=13
KEY_EXP=14
KEY_LN=15
KEY_LOG=16
KEY_IMAGINARY=17
KEY_COMMA=18
KEY_POWER=19
KEY_SINE=20
KEY_COSINE=21
KEY_TANGENT=22
KEY_PI=23
KEY_SQRT=24
KEY_SQUARE=25
KEY_SEVEN=26
KEY_EIGHT=27
KEY_NINE=28
KEY_LEFTPARENTHESIS=29
KEY_RIGHTPARENTHESIS=30
KEY_FOUR=31
KEY_FIVE=32
KEY_SIX=33
KEY_MULTIPLICATION=34
KEY_DIVISION=35
KEY_ONE=36
KEY_TWO=37
KEY_THREE=38
KEY_PLUS=39
KEY_MINUS=40
KEY_ZERO=41
KEY_DOT=42
KEY_EE=43
KEY_ANS=44
KEY_EXE=45
KEYS=[
  "left","up","down","right","return","del","home","end","shift","ctrl",":",";",
  "\"","backspace","[","]","{","}",",","^","s","c","t","p","<","²","7","8","9",
  "(",")","4","5","6","*","/","1","2","3","+","-","0",".","insert","@","enter"
]
### ^ All keys of Numworks ^ ###

from keyboard import is_pressed
def keydown(key):
  try: return is_pressed(KEYS[key])
  except IndexError: raise KeyError("key not found.")

def getAllKeys(): return KEYS

def getKey(key): 
  try: return KEYS[key]
  except IndexError: raise KeyError("key not found.")

"""
# v It's just for testing my code.
while True:
  if keydown(KEY_HOME):
    break
"""
