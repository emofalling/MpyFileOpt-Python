import sys
if sys.version_info < (3, 10):
    raise RuntimeError("Python 3.10 or later is required. That are not supported feautures below Python 3.10 (not include Python 3.10) include:\n"
                       "    Advanced Type Annotation (type_a | type_b, type[types], and more), match-case, and more")

from .mpyfopt import *
from .mpyfopt import __version__, __author__
