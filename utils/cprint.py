'''
cprint module to color print

color can be disabled by setting 'False' in env['COLORED']
'''

import os
from termcolor import cprint as term_cprint


def cprint(*text, color=None, on_color=None, attrs=None, **kwargs):
    '''
    color print
    '''
    if os.environ.get('COLORED') == 'False':
        print(*text, **kwargs)
    else:
        text_together = ' '.join(text)
        term_cprint(text_together, color, on_color, attrs, **kwargs)
