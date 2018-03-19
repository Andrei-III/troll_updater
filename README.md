# TrollPatch Updater
Simple patching &amp; updating utility for Mount &amp; Blade Warband NeoGK mod with TrollGame flavour.
Written in Python 2.7 and compiled to executable with py2exe v0.6.9 .

Features:

The tool will talk to the troll-game.org server to find out the latest version of neogk patch available for download (if it cannot connect to the server for various reasons, it will notify the user and ask him to try again later).

If warband installation is not found in the Windows registry, the program will exit.

Before installing or updating the patch, if the Native module is found, a backup is created automatically inside the Modules folder with the following format: Native_Backup_YYYY-MM-DD.zip

The tool can also fetch the latest versions of the TrollGame addons and install them.

Hashes:

MD5:     F32B640DD837E42755C689C4FA918779

SHA-1:   7C5FB806230DA8F42BE6F55EE1A9492DC494E3DD

SHA-256: CE1A4F7981A8C062D42B747178F8D89640E160246488AC273F1E9C8DD1C7E464
