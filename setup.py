import sys
import py2exe
from distutils.core import setup

sys.argv.append('py2exe')

# bundle_files = bundle dlls in the zipfile or the exe.
# Valid values for bundle_files are:
# 3 = don't bundle (default)
# 2 = bundle everything but the Python interpreter
# 1 = bundle everything, including the Python interpreter

setup(
    options={'py2exe': {'bundle_files': 1, 'compressed': True}},
    console=[
        {
            "script": "troll_updater.py",
            "icon_resources": [(0, "troll_updater.ico")],
            "dest_base": "troll_updater"
        }
    ],
    zipfile=None, requires=['colorama']
)
