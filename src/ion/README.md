![Visitor Badge](https://visitor-badge.laobi.icu/badge?page_id=ZetaMap.Ion-Numworks) ![Downloads](https://shields.io/github/downloads/ZetaMap/Ion-Numworks/total) ![pip](https://img.shields.io/pypi/dm/ion-numworks?label=pip_downloads)

# Ion-numworks
This is just a little low level library for fetching keyboard input. <br>
This is a porting of the Numworks module, and add other methods created by others OS (like Omega or Upsilon).

### Installation
You can download it on [pypi.org](https://pypi.org/project/ion-numworks), download files of the [latest release](https://github.com/ZetaMap/Ion-numworks/releases/latest). <br>
Or simply run this command to install library: ``pip install ion-numworks``

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
| right        | Right        | KEY_RIGHT            | 1
| down         | Down         | KEY_DOWN             | 2
| up           | Up           | KEY_UP               | 3
| OK           | Insert       | KEY_OK               | 4
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
| EXE          | Return       | KEY_EXE              | 52

### Additional features
#### Environ options
**/!\\ You must make its additions *before* importing ion otherwise the changes will not take effect! /!\\**

You can also change some default option of library. *(Options names are the same as Kandinsky library so that, if both libraries are present, they are synchronized)*<br> 
To do this, first import the environ of os module like this: ``import os``.

* Change starting OS (methods according to the selected os will be created):
```python
# '0': All methods
# '1': Numworks methods
# '2': Omega method
# '3': Upsilon methods
os.environ['KANDINSKY_OS_MODE'] = '<number>'
```