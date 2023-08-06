import sys
from .test_tools import *

sys.modules.update({f'{__name__}.{m}': globals()[m] for m in ['plt']})