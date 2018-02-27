# TrollPatch Updater
Simple patching &amp; updating utility for Mount &amp; Blade Warband NeoGK mod with TrollGame flavour.
Written in Python 2.7 and compiled to executable with py2exe v0.6.9 .

The tool will talk to the troll-game.org server to find out the latest version of neogk patch available for download (if it cannot connect to the server for various reasons, it will notify the user and ask him to try again later).

If warband installation is not found in the Windows registry, the program will exit.

Before installing or updating the patch, if the Native module is found, a backup is created automatically inside the Modules folder with the following format: Native_Backup_YYYY-MM-DD.zip


Hashes:

MD5:     1B17B9433C7D208C41046575D2F5802D

SHA-1:   DE04D714EFE7CF83F17C55A8ADCC9E06AAA5E16A

SHA-256: ACFA51C102F6E551483B0C792347B14EB8FAAF2DB3FDED535C747FBC5F8D7410
