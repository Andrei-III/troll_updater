from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

setup(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    console = [
        {
            "script": "troll_updater.py",
            "icon_resources": [(0, "troll_updater.ico")],
            "dest_base":"troll_updater"
        }
    ],
    zipfile = None,
)