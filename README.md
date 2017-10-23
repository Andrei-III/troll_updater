# TrollPatch Updater
Simple patching &amp; updating utility for Mount &amp; Blade Warband

The tool will talk to the troll-game.org server to find out the latest version of neogk patch available for download (if it cannot connect to the server for various reasons, it will notify the user and ask him to try again later).

If warband installation is not found in the Windows registry, the program will exit.

If Warband installation is found and the patch is not detected it will ask the user if he / she wants to install it.

If Warband installation is found and the patch is detected, it will compare the version to the latest one available and if neccessary, it will ask the user if he / she wants to update to the latest version.

Before installing or updating the patch, if the Native module is found, a backup is created automatically inside the Modules folder with the following format: Native_Backup_YYYY-MM-DD.zip
