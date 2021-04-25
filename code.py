import keyboard
import os
import requests
import time as Clock

## Player List
players = list()

## Config Variables
chars = " !\"#$&'()*-+,./0123456789:;<=>?@[\\]^_{}|~abcdefghijklmnopqrstuvwxyzбвгджзклмнпрстфхцчшщаеёиоуыэюяйьъ"
path = "C:/Program Files (x86)/Steam/steamapps/common/Team Fortress 2"
botnames = list()
botsteamids = list()
output_player = False
output_votekick = True
clear_log = True
online_database = True
sleep_time = 5
status_keybind = 71
votekick_keybind = 72
tf2_status_keybind = "KP_HOME"
tf2_votekick_keybind = "KP_UPARROW"

key_convert = {
    "LWIN":91,
    "RALT":541,
    "RCTRL":29,
    "SCROLLLOCK":70,
    "PGDN":81,
    "UPARROW":72,
    "LEFTARROW":75,
    "DOWNARROW":80,
    "RIGHTARROW":77,
    "KP_SLASH":53,
    "KP_MULTIPLY":55,
    "KP_MINUS":74,
    "KP_HOME":71,
    "KP_UPARROW":72,
    "KP_PGUP":73,
    "KP_PLUS":78,
    "KP_LEFTARROW":75,
    "KP_5":76,
    "KP_RIGHTARROW":77,
    "KP_END":79,
    "KP_DOWNARROW":80,
    "KP_PGDN":81,
    "KP_ENTER":28,
    "KP_INS":82,
    "KP_DEL":83
}

# This is used to convert a string with the format hh:mm:ss (or mm:ss) to an integer
def timetoint(time):
    try:
        total = 0
        times = time.split(":")
        if len(times) == 2:
            total = (int(times[0])*60)+int(times[1])
        elif len(times) == 3:
            total = (int(times[0])*3600)+(int(times[1])*360)+int(times[2])
        return total
    except:
        return 0

def votekick(player):
    try:
        #If we enabled the outputting of votekicks, the console will print a message
        if output_votekick:
            print("Votekicking " + str(player))
        # We open our votekick file, and write the desired command to kick the bot inside
        with open(path + "/tf/cfg/votekick.cfg", "w", encoding="utf-8", errors="ignore") as f:
            f.write("callvote kick " + str(player.userid))
            f.close()
        # We wait a bit so everything can catch up to speed
        Clock.sleep(1)
        # We send a key press to the system, which TF2 will read.
        keyboard.send(votekick_keybind)
        # TF2 will respond by executing the cfg file, and votekicking the bot
        Clock.sleep(5)
    except:
        # Sometimes if we update the file too fast, we can get a PermissionError
        # If this is the case, we simply wait for a while and try again later
        print("PermissionError, waiting")
        Clock.sleep(10)

# This is used to find the player with the shortest connectiom time with the name of variable 'name'
def getnewest(name):
    duplicates = list()
    # We query through every player
    for player in players:
        #If the player has the name we're searching for, we add it to the list
        if player.name == name:
            duplicates.append(player)
    
    newestplayer = duplicates[0]
    # Next we go through every player, and if the player has a shorter connection time than our current value,
    # We set the newestplayer variable to the new player
    for duplicate in duplicates:
        if duplicate.time <= newestplayer.time:
            newestplayer = duplicate
    return newestplayer

# This is a simple class instance which holds some basic player info
class PlayerInstance:
    
    userid = 0
    name = ""
    time = 0
    steamid = ""

    def __init__(self, userid, name, time, steamid):
        self.userid = userid
        self.name = name
        self.time = time
        self.steamid = steamid
        
    def __str__(self):
        return "PlayerInstance[userid:" + str(self.userid) + ",name:" + self.name + ",time:" + str(self.time) + ",steamid:" + self.steamid + "]"

def setup():
    global tf2_status_keybind
    global tf2_votekick_keybind
    with open("config.properties", "r",encoding="utf-8") as f:
        config = f.readlines()
    for line in config:
        if not line.startswith("#") and not line == "":
            splitter = line.find("=")
            key = line[:splitter]
            value = line[splitter+1:].replace("\n","")
            if key == "path":
                global path
                path = value
            elif key == "chars":
                global chars
                chars = value
            elif key == "output_player":
                global output_player
                output_player = value.lower().startswith("t")
            elif key == "output_votekick":
                global output_votekick
                output_votekick = value.lower().startswith("t")
            elif key == "clear_log":
                global clear_log
                clear_log = value.lower().startswith("t")
            elif key == "sleep_time":
                global sleep_time
                sleep_time = int(value)
            elif key == "status_keybind":
                global status_keybind
                status_keybind = key_convert.get(value, value)
                tf2_status_keybind = value
            elif key == "votekick_keybind":
                global votekick_keybind
                votekick_keybind = key_convert.get(value, value)
                tf2_votekick_keybind = value
            elif key == "online_database":
                global online_database
                online_database = value.lower().startswith("t")
            else:
                print("Ignoring key '" + key + "'")
        
        if os.path.isfile(path + "/tf/cfg/autoexec.cfg"):
            with open(path + "/tf/cfg/autoexec.cfg", "r", encoding="utf-8") as f:
                lines = f.readlines()
            with open(path + "/tf/cfg/autoexec.cfg", "w", encoding="utf-8") as f:
                found_status_keybind = False
                found_votekick_keybind = False
                for line in lines:
                    write_line = True
                    if line.startswith("bind \""):
                        if line.endswith("\" \"status\"\n"):
                            if line == "bind \"" + tf2_status_keybind + "\" \"status\"\n":
                                found_status_keybind = True
                            else:
                                write_line = False
                        elif line.endswith("\" \"exec votekick.cfg\""):
                            if line == "bind \"" + tf2_votekick_keybind + "\" \"exec votekick.cfg\"":
                                found_votekick_keybind = True
                            else:
                                write_line = False
                    if write_line:
                        f.write(line)
                if not found_status_keybind:
                    f.write("\nbind \"" + tf2_status_keybind + "\" \"status\"")
                if not found_votekick_keybind:
                    f.write("\nbind \"" + tf2_votekick_keybind + "\" \"exec votekick.cfg\"")
        else:
            with open(path + "/tf/cfg/autoexec.cfg", "w", encoding="utf-8") as f:
                f.write("bind \"" + tf2_status_keybind + "\" \"status\"\n")
                f.write("bind \"" + tf2_votekick_keybind + "\" \"exec votekick.cfg\"")
    with open(path + "/tf/console.log", "w", encoding="utf-8", errors="ignore") as f:
        f.close()

def get_bots():
    global botnames
    global botsteamids
    global online_database
    if online_database:
        online_file = requests.get("https://raw.githubusercontent.com/boyonkgit/tf2-bot-kicker/main/bots.properties").text.split("\n")
        for line in online_file:
            if not line.startswith("#") and not line == "":
                splitter = line.find("=")
                key = line[:splitter]
                value = line[splitter+1:].replace("\n","")
                if key == "name":
                    botnames.append(value)
                elif key == "steamid":
                    botsteamids.append(value)
                else if not key == "xname" and not key == "xsteamid":
                    print("Ignoring key '" + key + "' in online database (do you have an outdated version?)")

    with open("bots.properties", "r",encoding="utf-8") as f:
        bots_file = f.readlines()
    for line in bots_file:
        if not line.startswith("#") and not line == "":
            splitter = line.find("=")
            key = line[:splitter]
            value = line[splitter+1:].replace("\n","")
            if key == "name":
                botnames.append(value)
            elif key == "steamid":
                botsteamids.append(value)
            elif key == "xname":
                try:
                    botnames.remove(value)
                except:
                    print("Name '" + value + "' was not found in list")
            elif key == "xsteamid":
                try:
                    botsteamids.remove(value)
                except:
                    print("SteamID '" + value + "' was not found in list")
            else:
                print("Ignoring key '" + key + "' in bots.properties")



## Setup
setup()
get_bots()

## Main Loop
while True:
    Clock.sleep(sleep_time)
    
    ## Quering Status
    
    # We send a key press to the system, which TF2 will read.
    keyboard.send(status_keybind)
    Clock.sleep(1)
    # Because we bound this key to the command "status", TF2 will output the status in the console.
    # We then read the console from the console.log file (which we enabled TF2 to output to in our startup settings)
    with open(path + "/tf/console.log", "r", encoding="utf-8", errors="ignore") as f:
        console = f.readlines()
    #Next we clear the console.log file, so we can easily start reading for the next output
    with open(path + "/tf/console.log", "w", encoding="utf-8", errors="ignore") as f:
        f.close()
    
    ## Reading Console
    userids = list()
    new_players = list()
    
    # We go through every line in the console
    for line in console:
        # We know that players in the status command output are always prefixed with a '#'
        # By default TF2 will also output the column names in a line (which starts with "# userid"), if this is the case, we ignore it
        if line.startswith("#") and not line.startswith("# userid"):
            arguments = list()
            # We split the line with ' ' (space)
            for part in line.rstrip().split(" "):
                # If the splitted part has characters (aka is not an empty string), we append it to the arguments
                if len(part) > 0:
                    arguments.append(part)
            # We make sure that we do not take official Valve bots in consideration (in casual these never appear, but in community servers they can)
            if not arguments[len(arguments)-2] == "BOT":
                # We know that our first argument is the userid of the player
                userid = arguments[1]
                if not userid in userids:
                    userids.append(userid)
                    # We also know that the playername starts after the first '\"' in the string and that it ends at the last '\"' in the string, so we take everything in between
                    original_name = line[line.find("\"")+1:line.rfind("\"")]
                    name = ""
                    # We then go through every character in the original name, if it is not in our allowed chars set, we skip it
                    for c in original_name:
                        if c.lower() in chars:
                            name = name + c.lower()
                    # We then read the formatted time from the string and convert it into a number in seconds
                    time = timetoint(arguments[len(arguments)-4])
                    
                    steamid = arguments[len(arguments)-5]
                    # Lastly we create and append the new Player Instance
                    new_players.append(PlayerInstance(userid,name,time,steamid))
                    
    # If we found any new players in our console, we will update the player list to all the players we found
    if len(new_players) > 0:
        players = new_players
    
    ## Bot Detecting
    
    checked_names = list()
    
    # We empty the log if enabled
    if clear_log:
        os.system("cls")
    
    # Next we go through every PlayerInstance in the list
    for player in players:
        # If we enabled the printing of players, we do so
        if output_player:
            print(str(player))
        # If the name of the player is in our list of botnames, we kick it
        # Else if the steamid of the player is in our list of botsteamids, we kick it
        # Else if the name of the player matches another player name we already went over, we vote kick the newest player
        # Else (if nothing is wrong) we append the name to the list of checked players
        if player.name in botnames:
            votekick(player)
        elif player.steamid in botsteamids:
            votekick(player)
        elif player.name in checked_names:
            votekick(getnewest(player.name))
        else:
            checked_names.append(player.name)