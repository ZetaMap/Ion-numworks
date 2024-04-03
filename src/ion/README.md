![Visitor Badge](https://visitor-badge.laobi.icu/badge?page_id=ZetaMap.Ion-Numworks) ![Downloads](https://shields.io/github/downloads/ZetaMap/Ion-Numworks/total) ![pip](https://img.shields.io/pypi/dm/ion-numworks?label=pip_downloads)

# Ion-numworks
This is just a little low level library for fetching keyboard input. <br>
This is a porting of the Numworks module, and add other methods created by others OS (like Omega or Upsilon).

### Installation
You can download it on [pypi.org](https://pypi.org/project/ion-numworks), download files of the [latest release](https://github.com/ZetaMap/Ion-numworks/releases/latest). <br>
Or simply run this command to install library: ``pip install --pre ion-numworks``

Also if you want to do it yourself, use this command to build and install the library automatically: ``python -m build && pip install .``

### More
Also i created the [Kandinsky module of Numworks](https://github.com/ZetaMap/Kandinsky-Numworks)

### Usable content
#### ***Numworks and Omega methods***

**keydown():**
* Parameters: ``k``
* Description: Return True if the ``k`` key is pressed (not release)

#### ***Upsilon methods (previous are also added)***

**get_keys():**
* Parameters: **No parameters**
* Description: Get name of pressed keys

**battery():**
* Parameters: **No parameters**
* Description: Return battery voltage

**battery_level():**
* Parameters: **No parameters**
* Description: Return battery level

**battery_ischarging():**
* Parameters: **No parameters**
* Description: Return True if the battery is charging

**set_brightness():**
* Parameters: ``level``
* Description: Set brightness level of screen

**get_brightness():**
* Parameters: **No parameters**
* Description: Get brightness level of screen

#### ***Associated keyboard keys***

| Numworks key | Computer key | Field name           | Field value
|:-------------|:-------------|:---------------------|:------------
| left         | Left         | KEY_LEFT             | 0
| up           | Up           | KEY_UP               | 1
| down         | Down         | KEY_DOWN             | 2
| right        | Right        | KEY_RIGHT            | 3
| OK           | Return       | KEY_OK               | 4
| back         | Delete       | KEY_BACK             | 5
| home         | Escape       | KEY_HOME             | 6
| onOff        | End          | KEY_ONOFF            | 7
| shift        | Shift        | KEY_SHIFT            | 12
| alpha        | CTRL         | KEY_ALPHA            | 13
| xnt          | X            | KEY_XNT              | 14
| var          | V            | KEY_VAR              | 15
| toolbox      | "            | KEY_TOOLBOX          | 16
| backspace    | Backspace    | KEY_BACKSPACE        | 17
| exp          | E            | KEY_EXP              | 18
| ln           | N            | KEY_LN               | 19
| log          | L            | KEY_LOG              | 20
| imaginary    | I            | KEY_IMAGINARY        | 21
| comma        | ,            | KEY_COMMA            | 22
| power        | ^            | KEY_POWER            | 23
| sin          | S            | KEY_SINE             | 24
| cos          | C            | KEY_COSINE           | 25
| tan          | T            | KEY_TANGENT          | 26
| pi           | P            | KEY_PI               | 27
| sqrt         | R            | KEY_SQRT             | 28
| square       | >            | KEY_SQUARE           | 29
| 7            | 7            | KEY_SEVEN            | 30
| 8            | 8            | KEY_EIGHT            | 31
| 9            | 9            | KEY_NINE             | 32
| (            | (            | KEY_LEFTPARENTHESIS  | 33
| )            | )            | KEY_RIGHTPARENTHESIS | 34
| 4            | 4            | KEY_FOUR             | 36
| 5            | 5            | KEY_FIVE             | 37
| 6            | 6            | KEY_SIX              | 38
| *            | *            | KEY_MULTIPLICATION   | 39
| /            | /            | KEY_DIVISION         | 40
| 1            | 1            | KEY_ONE              | 42
| 2            | 2            | KEY_TWO              | 43
| 3            | 3            | KEY_THREE            | 44
| +            | +            | KEY_PLUS             | 45
| -            | -            | KEY_MINUS            | 46
| 0            | 0            | KEY_ZERO             | 48
| .            | .            | KEY_DOT              | 49
| EE           | !            | KEY_EE               | 50
| Ans          | A            | KEY_ANS              | 51
| EXE          | Insert       | KEY_EXE              | 52

### Additional features
#### Environ options
**/!\\ You must make its additions *before* importing ion otherwise the changes will not take effect! /!\\**

You can also change some default option of library.<br>
To do this, first import os module and add a compatibility check, like this:
```python
try:
  import os
  if hasattr(os, "environ"):
    "<environ options here>"
except: pass
```

* Change starting OS (methods according to the selected os will be created): <br>
*(Option name is same as Kandinsky so that, if both libraries are present, they are synchronized)*
```python
# '0': All methods
# '1': Numworks methods
# '2': Omega method
# '3': Upsilon methods
os.environ['KANDINSKY_OS_MODE'] = '<number>'
```

* Or if you want to not synchronize the library with kandinsky, use this environ name:
```python
os.environ['ION_OS_MODE'] = '<number>'
```

* Enable debug mode:
```python
# Print full error stacktrace, the original pressed key and methods calls
os.environ['ION_ENABLE_DEBUG'] = ''
```

* Disable warnings:
```python
# Will be disable all ion warnings
os.environ['ION_DISABLE_WARNINGS'] = ''
```

* Disable reading inputs only in kandinsky window (if kandinsky is not imported globally, this option is enabled by default):
```python
# This options allow to read keyboard inputs in python console and kandinsky window
# By default it just read kandinsky window (only if is focused)
# Note: if is not imported globally, this option is enabled by default
os.environ['ION_DISABLE_KANDINSKY_INPUT_ONLY'] = ''
```

* Get keyboard inputs everywhere (not only in kandinsky window or python console):
```python
# Allow to get inputs in entire system, like previous version of library
os.environ['ION_ENABLE_GET_INPUT_EVERYWHERE'] = ''
```
