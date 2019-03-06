# TrollPatch Updater
Simple patching &amp; updating utility for Mount &amp; Blade Warband NeoGK mod with TrollGame flavour.
Written in Python 2.7 and compiled to executable with py2exe v0.6.9 .

Features:

The tool will talk to the troll-game.org server to find out the latest version of neogk patch available for download (if it cannot connect to the server for various reasons, it will notify the user and ask him to try again later).

If warband installation is not found in the Windows registry, the program will exit.

Before installing or updating the patch, if the Native module is found, a backup is created automatically inside the Modules folder with the following format: Native_Backup_YYYY-MM-DD.zip

The tool can also fetch the latest versions of the TrollGame addons and install them.

Hashes:

MD5:     37524c37f33547623afc196177af1968

SHA-1:   e78a111662d15c5dc6782e22f6c4f145cf86a3a1

SHA-256: 1a86e97775d5d32613ecf99700472a5a839c09b3130bf616dd2ffb012cd46698
