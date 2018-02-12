# TrollPatch Updater
Simple patching &amp; updating utility for Mount &amp; Blade Warband NeoGK mod with TrollGame flavour.
Written in Python 2.7 and compiled to executable with pyinstaller.

The tool will talk to the troll-game.org server to find out the latest version of neogk patch available for download (if it cannot connect to the server for various reasons, it will notify the user and ask him to try again later).

If warband installation is not found in the Windows registry, the program will exit.

If Warband installation is found and the patch is not detected it will ask the user if he / she wants to install it.

If Warband installation is found and the patch is detected, it will compare the version to the latest one available and if neccessary, it will ask the user if he / she wants to update to the latest version.

Before installing or updating the patch, if the Native module is found, a backup is created automatically inside the Modules folder with the following format: Native_Backup_YYYY-MM-DD.zip


Hashes:

MD5:     6C74CDF4569E3A513B7D291E159E279E

SHA-1:   E05ADC2A2462456499F9990469B6F12863E53502

SHA-256: 92C1EE1EC2D4A9530C746B13C8209B69E3A1F79A70BBE1BC39C250A9E8A90ADB
