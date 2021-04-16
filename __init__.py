"""
This is the adaptation of Ion module of Numworks.
Please don't use keyboard and this module at the same time.
"""
### v All keys of Numworks v ###
KEY_LEFT="left"
KEY_UP="up"
KEY_DOWN="down"
KEY_RIGHT="right"
KEY_OK="return"
KEY_BACK="del"
KEY_HOME="home"
KEY_ONOFF="end"
KEY_SHIFT="shift"
KEY_ALPHA="ctrl"
KEY_XNT=":"
KEY_VAR=";"
KEY_TOOLBOX="\""
KEY_BACKSPACE="backspace"
KEY_EXP="["
KEY_LN="]"
KEY_LOG="{"
KEY_IMAGINARY="}"
KEY_COMMA=","
KEY_POWER="^"
KEY_SINE="s"
KEY_COSINE="c"
KEY_TANGENT="t"
KEY_PI="="
KEY_SQRT="<"
KEY_SQUARE="²"
KEY_SEVEN="7"
KEY_EIGHT="8"
KEY_NINE="9"
KEY_LEFTPARENTHESIS="("
KEY_RIGHTPARENTHESIS=")"
KEY_FOUR="4"
KEY_FIVE="5"
KEY_SIX="6"
KEY_MULTIPLICATION="*"
KEY_DIVISION="/"
KEY_ONE="1"
KEY_TWO="2"
KEY_THREE="3"
KEY_PLUS="+"
KEY_MINUS="-"
KEY_ZERO="0"
KEY_DOT="."
KEY_EE="insert"
KEY_ANS="@"
KEY_EXE="enter"
### ^ All keys of Numworks ^ ###

from keyboard import is_pressed
def keydown(k):
  return is_pressed(k)

"""
# v It's just for testing my code.
while True:
  if keydown(KEY_HOME):
    break
"""
