import warnings
warnings.filters = [] # Reset filters because some default appear in, and HIS DON'T PRINT MY WARNINGS!!

# prettywarn method of pysdl2
def prettywarn(message, warntype=None): 
    """Prints a suppressable warning without stack or line info."""
    original = warnings.formatwarning
    warnings.formatwarning = lambda message, category, *_: f"{category.__name__}: {message}\n"
    warnings.warn(message, warntype)
    warnings.formatwarning = original
