from .production import *
from .logging import *
from .oauth import *
from .features import ENABLED_FEATURES
try:
    from .local import *
    if 'DISABLED_APPS' in locals():
        INSTALLED_APPS = [k for k in INSTALLED_APPS if k not in DISABLED_APPS]
except ImportError:
    pass
