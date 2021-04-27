# tf2-bot-kicker by boyonk

### Love this? Wanna give something back? [buy me a coffee!](https://www.buymeacoff.ee/boyonk)

#### This bot kicker will be updated regularly, so make sure to check back here every week or so!
#### I'm planning on implementing more code for different bot types, an online database, and an auto-updater

## REQUIREMENTS
- [Python 3 (or later)](https://www.python.org/downloads/)

## SETUP
1. Download everything from [here](https://github.com/boyonkgit/tf2-bot-kicker/archive/refs/heads/main.zip)
2. Unzip the file in a folder
3. Startup Steam and go to your library
4. Right-click on Team Fortress 2
5. Click "Properties"
6. Go to "General"
7. Under "Launch Options" add `-condebug`
8. Configure `./config.properties` to your wishes (see below)
9. You're good to go! Simply run the script using `start.bat`!

## CONFIGURING CONFIG.PROPERTIES
Open the config.properties file with a simple text editor (I prefer Notepad++, regular Notepad will work as well)
If there isn't anything specific you want to change and just want to make sure it runs, you only need to worry about the 'path' key.
This is done as follows:
1. Startup Steam and go to your library
2. Right-click on Team Fortress 2
3. Click "Properties"
4. Under "Local Files" click "Browse..."
5. Replace everything after 'path=' with the path to the folder you just opened
6. Save the file, and you're done!

## ADDING A BOT
If you want to a specific bot based on their name or their steamid, you can do so in the `./bots.properties` file. As with the config,
open it in a text editor and follow the documentation and styling to add a bot. If you truly believe the player is a hacker,
consider commenting on an existing report in the bugtracker with more evidence, or, if there hasn't been a report, [creating an issue](https://github.com/boyonkgit/tf2-bot-kicker/issues/new) with "REPORT: \<name or steamid\>" in the title of the issue.
If the report gets enough traction it will be added to the online database.

## WILL THIS GET ME BANNED?
No. And here's why:
- No code is changed on the client-side
- Every interaction with TF2 is done through the console and scripting, which is allowed
- This program simply automates and recreates what you would do manually, but does it faster

## HOW DOES IT WORK?
- The program sends a key press to the system, which TF2 will read.
- TF2 responds by outputting the result of the `status` command in the console.
- Because we enabled `-condebug` in our Launch Options, the output of the console will
be written to `/tf/console.log` in our TF2 files.
- We read the `/tf/console.log` and store all necessary information.
- Next, we go through the player list, and see if any name matches to the name of a bot
we specified in our `./config.properties`.
- We also check if any name is in the list twice, and if so, we get the player with the shortest
connection time.
- If a bot is found, we write the required command to votekick it in `tf/cfg/votekick.cfg`.
After that, we send a different key press to the system, which TF2 will read.
- TF2 will respond by executing the command stored in `tf/cfg/votekick.cfg` and starting a votekick.

### I wanna know more!
You can also look in `./code.py` where I commented on what every piece of code does, so you can
look in detail on how it works.

## HELP! IT DOESN'T WORK!
Oh no! Look through the bugtracker and see if your issue can be found there. If not, consider [creating an issue](https://github.com/boyonkgit/tf2-bot-kicker/issues/new) and I'll try and get back to you.

## I WANT TO CONTRIBUTE TO / ADAPT / CHANGE THE CODE
Amazing! All help is appreciated! Consider forking the project and changing what you believe needs to be changed. Make sure you follow [the license](https://github.com/boyonkgit/tf2-bot-kicker/blob/main/LICENSE.md).

## AMAZING CONTRIBUTORS
- michaelshumshum
