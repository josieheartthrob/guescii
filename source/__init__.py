
# Implemented support for other platforms
from sys import platform

def _get_clear_word():
    if platform == 'win32':
        return 'cls'
    else:
        return 'clear'

clear = _get_clear_word()
