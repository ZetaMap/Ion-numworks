![Visitor Badge](https://visitor-badge.laobi.icu/badge?page_id=ZetaMap.Ion-Numworks) ![Downloads](https://shields.io/github/downloads/ZetaMap/Ion-Numworks/total) ![pip](https://img.shields.io/pypi/dm/ion-numworks?label=pip_downloads)

# Ion-numworks
This is just a little low level library for fetching keyboard input. <br>
This is a porting of the Numworks module, and add other methods created by others OS (like Omega or Upsilon).


### Installation
You can download it on [pypi.org](https://pypi.org/project/ion-numworks), download files of the [latest release](https://github.com/ZetaMap/Ion-numworks/releases/latest), or simply run this command to install library: ``pip install ion-numworks``. <br>
To install from local folder, use: ``pip install .``


### More
I also created the porting of the [Numworks' Kandinsky module](https://github.com/ZetaMap/Kandinsky-Numworks)


### API methods
*Numworks and Omega methods*

#### keydown():
* Parameters: ``k``
* Description: Return True if the ``k`` key is pressed (not release)

<br>

*Upsilon-specific methods (previous are also added)*

#### get_keys():
* Parameters: **No parameters**
* Description: Get name of pressed keys

#### battery():
* Parameters: **No parameters**
* Description: Return battery voltage *(give a fake result)*

#### battery_level():
* Parameters: **No parameters**
* Description: Return battery level *(give a fake result)*

#### battery_ischarging():
* Parameters: **No parameters**
* Description: Return True if the battery is charging *(give a fake result)*

#### set_brightness():
* Parameters: ``level``
* Description: Set brightness level of screen *(do nothing)*

#### get_brightness():
* Parameters: **No parameters**
* Description: Get brightness level of screen


### Numworks keyboard association
| Numworks key | Computer key      | Field name           | Field value
|:-------------|:------------------|:---------------------|:------------
| left         | ⯇  (Left)         | KEY_LEFT             | 0
| up           | ⯅  (Up)           | KEY_UP               | 1
| down         | ⯆  (Down)         | KEY_DOWN             | 2
| right        | ⯈  (Right)        | KEY_RIGHT            | 3
| OK           | **⮠**  (Return)       | KEY_OK               | 4
| back         | Delete            | KEY_BACK             | 5
| home         | Escape            | KEY_HOME             | 6
| onOff        | End               | KEY_ONOFF            | 7
| shift        | **⇧**  (Shift)        | KEY_SHIFT            | 12
| alpha        | CTRL              | KEY_ALPHA            | 13
| xnt          | X                 | KEY_XNT              | 14
| var          | V                 | KEY_VAR              | 15
| toolbox      | "                 | KEY_TOOLBOX          | 16
| backspace    | **🠄**  (Backspace)    | KEY_BACKSPACE        | 17
| exp          | E                 | KEY_EXP              | 18
| ln           | N                 | KEY_LN               | 19
| log          | L                 | KEY_LOG              | 20
| imaginary    | I                 | KEY_IMAGINARY        | 21
| comma        | ,                 | KEY_COMMA            | 22
| power        | ^                 | KEY_POWER            | 23
| sin          | S                 | KEY_SINE             | 24
| cos          | C                 | KEY_COSINE           | 25
| tan          | T                 | KEY_TANGENT          | 26
| pi           | P                 | KEY_PI               | 27
| sqrt         | R                 | KEY_SQRT             | 28
| square       | >                 | KEY_SQUARE           | 29
| 7            | 7                 | KEY_SEVEN            | 30
| 8            | 8                 | KEY_EIGHT            | 31
| 9            | 9                 | KEY_NINE             | 32
| (            | (                 | KEY_LEFTPARENTHESIS  | 33
| )            | )                 | KEY_RIGHTPARENTHESIS | 34
| 4            | 4                 | KEY_FOUR             | 36
| 5            | 5                 | KEY_FIVE             | 37
| 6            | 6                 | KEY_SIX              | 38
| *            | *                 | KEY_MULTIPLICATION   | 39
| /            | /                 | KEY_DIVISION         | 40
| 1            | 1                 | KEY_ONE              | 42
| 2            | 2                 | KEY_TWO              | 43
| 3            | 3                 | KEY_THREE            | 44
| +            | +                 | KEY_PLUS             | 45
| -            | -                 | KEY_MINUS            | 46
| 0            | 0                 | KEY_ZERO             | 48
| .            | .                 | KEY_DOT              | 49
| EE           | !                 | KEY_EE               | 50
| Ans          | A                 | KEY_ANS              | 51
| EXE          | Insert *(For MacOS: Shift+Return)*           | KEY_EXE              | 52


### Environ variables
> [!IMPORTANT]
> You must make these additions before importing the ion module, otherwise the changes will not take effect.

Some library options can be modified by environ variables.<br>
To do so, add a compatibility check and place the environ variables into:
```python
try:
  import os
  "<environ variables here>"
except: pass
```

<br>

* Change starting OS (methods according to the selected os will be created): <br>
*(Option name is same as Kandinsky so that, if both libraries are present, they are synchronized)*
```python
# '0': All methods
# '1': Numworks methods
# '2': Omega method
# '3': Upsilon methods
os.environ['KANDINSKY_OS_MODE'] = '<number>'
```

* Or if you don't want to synchronize the library with kandinsky, use this environ name:
```python
os.environ['ION_OS_MODE'] = '<number>'
```

* Enable debug mode:
```python
# Print full error stacktrace, the pressed key and methods calls
os.environ['ION_ENABLE_DEBUG'] = ''
```

* Disable warnings:
```python
# Will disable all ion warnings, like not found windows or incompatibilities.
os.environ['ION_DISABLE_WARNINGS'] = ''
```

* Disable inputs reading only from the kandinsky window:
```python
# This options allow keyboard inputs reading from the python console and the kandinsky window
# By default it only reads the kandinsky window (only if focused by user)
# Note: if kandinsky is not imported globally, this option is enabled by default
os.environ['ION_DISABLE_KANDINSKY_INPUT_ONLY'] = ''
```

* Get keyboard inputs everywhere (not only from kandinsky window or python console):
```python
# Allow to get inputs from entire system, like previous version of library
os.environ['ION_ENABLE_GET_INPUT_EVERYWHERE'] = ''
```
