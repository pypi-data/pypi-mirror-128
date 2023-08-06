from importlib import reload as _reload
from .poset import *

# keys = [  # Order may matter
#     'poset_exceptions',
#     'poset_wbools',
#     'help_index',
#     'algorithm_random_poset_czech',
#     'posets',
# ]

# def reload(module):
#     assert module.__name__ == 'cp93posets'
#     for key in keys:
#         _reload(getattr(module, key))
#     _reload(module)
#     print('Module reloaded')
#     return