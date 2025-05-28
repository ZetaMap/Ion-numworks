import warnings
warnings.filters = [] # Reset filters because some default appear in, and HIS DON'T PRINT MY WARNINGS!!

WARNINGS = False
def set_warnings(enabled):
  global WARNINGS
  WARNINGS = enabled

# prettywarn method of pysdl2
def prettywarn(message, warntype=None):
  """Prints a suppressable warning without stack or line info."""
  if not WARNINGS: return
  original = warnings.formatwarning
  warnings.formatwarning = lambda message, category, *_: f"{category.__name__}: {message}\n"
  warnings.warn(message, warntype)
  warnings.formatwarning = original

DEBUG = False
def set_debug(enabled):
  global DEBUG
  DEBUG = enabled
  
def is_debug():
  return DEBUG

def print_debug(type, *msgs, **print_args):
  if DEBUG:
    if "end" in print_args and not print_args["end"].startswith('\n'): print_args["end"] += '\n'
    print(f"DEBUG: {type}: ", end='')
    print(*msgs, **print_args)