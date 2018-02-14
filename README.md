# TrollPatch Updater
Simple patching &amp; updating utility for Mount &amp; Blade Warband NeoGK mod with TrollGame flavour.
Written in Python 2.7 and compiled to executable with py2exe v0.6.9 .

The tool will talk to the troll-game.org server to find out the latest version of neogk patch available for download (if it cannot connect to the server for various reasons, it will notify the user and ask him to try again later).

If warband installation is not found in the Windows registry, the program will exit.

Before installing or updating the patch, if the Native module is found, a backup is created automatically inside the Modules folder with the following format: Native_Backup_YYYY-MM-DD.zip


Hashes:

MD5:     2721FE80599A156E82647139C5D19B11

SHA-1:   44A62B5FE6FBD4BFD25647778237E75993D26EDC

SHA-256: 789DF747FD56D02A8350DF06CE14F98528D604B8E04D3420C769AC54A384C5B1
