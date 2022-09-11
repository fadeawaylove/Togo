import os
import sys

HOME_DIR = os.path.join(os.environ['USERPROFILE'] if sys.platform == 'win32' else os.environ['HOME'], ".togo")

os.makedirs(HOME_DIR, exist_ok=True)
