from .base import NoopFocusChecker, prettywarn, GET_INPUT_EVERYWHERE
import sys

__all__ = ["FocusChecker"]


if GET_INPUT_EVERYWHERE:
  class FocusChecker(NoopFocusChecker): ...

elif sys.platform.startswith("win"):
  from .win32 import FocusChecker
  
elif sys.platform.startswith("linux"):
  from .linux import FocusChecker
  
elif sys.platform.startswith("darwin"):
  #from .darwin import FocusChecker
  prettywarn("MacOS support is not finished, some features will be not present", ImportWarning)
  class FocusChecker(NoopFocusChecker): ...
  
else:
    # Platform not supported for focus, create an fake FocusChecker class
  # The 'focus on only window' will be disabled
  prettywarn(f"platform {sys.platform!r} not supported for focussed window inputs. "
              "Inputs will be gets on entire system", ImportWarning)
  class FocusChecker(NoopFocusChecker): ...
