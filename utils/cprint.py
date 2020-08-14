import os
from colorama import Fore, Style
from termcolor import cprint as term_cprint


def cprint(*text, color=None, on_color=None, attrs=None, **kwargs):
    if os.environ.get('COLORED') == 'False':
        print(*text, **kwargs)
    else:
        text_together = ' '.join(text)
        term_cprint(text_together, color, on_color, attrs, **kwargs)
