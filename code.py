import os
import keyboard
import re
import requests
from time import sleep
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0')

### variables ------ ###
players = list()
commands = list()
raw_console = list()

chars = " !\"#$&'()*-+,./0123456789:;<=>?@[\\]^_{}|~abcdefghijklmnopqrstuvwxyzбвгджзклмнпрстфхцчшщаеёиоуыэюяйьъ"
path = "/home/haywire/.local/share/Steam/steamapps/common/Team Fortress 2"
botnames = list()
botregexnames = list()
botsteamids = list()
output_player = False
output_votekick = True
clear_log = True
online_database = True
sleep_time = 5
query_keybind = 71
execute_keybind = 72
tf2_query_keybind = "KP_HOME"
tf2_execute_keybind = "KP_UPARROW"
auto_update = True

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
### ---------------- ###

### util ----------- ###
def time_to_int(time):
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


# This is used to find the player with the shortest connectiom time with the name of variable 'name'
def get_newest(name):
    global players
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

### classes -------- ###
class PlayerInstance:

    userid = 0
    name = ""
    time = 0
    steamid = ""

    def __init__(self, userid, name, time, steamid):
        print(name)
        self.userid = userid
        self.name = name
        self.time = time
        self.steamid = steamid

    def __str__(self):
        return "PlayerInstance[userid:" + str(self.userid) + ",name:" + self.name + ",time:" + str(self.time) + ",steamid:" + self.steamid + "]"

### ---------------- ###

### setup ---------- ###
def setup():
    read_config()
    check_update()
    setup_autoexec()
    create_bk_autoexec()
    create_bk_query()
    get_bots()


def read_config():
    with open("config.properties", "r",encoding="utf-8") as f:
        config = f.readlines()
    for line in config:
        if not line.startswith("#") and not line.strip() == "":
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
            elif key == "query_keybind" or key == "status_keybind":
                global query_keybind
                global tf2_query_keybind
                query_keybind = key_convert.get(value, value)
                print("get status")
                tf2_query_keybind = value
            elif key == "execute_keybind" or key == "votekick_keybind":
                global execute_keybind
                global tf2_execute_keybind
                execute_keybind = key_convert.get(value, value)
                tf2_execute_keybind = value
            elif key == "online_database":
                global online_database
                online_database = value.lower().startswith("t")
            elif key == "auto_update":
                global auto_update
                auto_update = value.lower().startswith("t")
            else:
                print("Ignoring key '" + key + "'")


def check_update():
    global auto_update
    if auto_update:
        files = list()
        files.append(requests.get("https://raw.githubusercontent.com/boyonkgit/tf2-bot-kicker/main/metadata.properties").text.split("\n"))
        with open("metadata.properties", "r",encoding="utf-8") as f:
            files.append(f.readlines())
        for i in range(len(files)):
            mapped = dict()
            file = files[i]
            for line in file:
                if not line.startswith("#") and not line.strip() == "":
                    splitter = line.find("=")
                    key = line[:splitter]
                    value = line[splitter+1:].replace("\n","")
                    if key == "version":
                        mapped[key] = value
            if i == 0:
                online_metadata = mapped
            else:
                metadata = mapped
        if not metadata["version"] == online_metadata["version"]:
            # update()
            pass


def update():
    new_metadata =  requests.get("https://raw.githubusercontent.com/boyonkgit/tf2-bot-kicker/main/metadata.properties").text.replace("\r","")
    new_code = requests.get("https://raw.githubusercontent.com/boyonkgit/tf2-bot-kicker/main/code.py").text.replace("\r","")

    with open("metadata.properties", "w", encoding="utf-8") as f:
        f.write(new_metadata)

    with open("code.py", "w", encoding="utf-8") as f:
        f.write(new_code)

    exec(open("code.py",encoding="utf-8").read())
    exit()
def setup_autoexec():
    if not os.path.isfile(path + "/tf/cfg/autoexec.cfg"):
        with open(path + "/tf/cfg/autoexec.cfg", "w", encoding="utf-8") as f:
            f.close()

    with open(path + "/tf/cfg/autoexec.cfg", "r", encoding="utf-8") as f:
        lines = f.readlines()
    bk_autoexec_found = False
    for line in lines:
        if line.startswith("exec \"bk_autoexec.cfg\""):
            bk_autoexec_found = True
            break
    if not bk_autoexec_found:
        with open(path + "/tf/cfg/autoexec.cfg", "a", encoding="utf-8") as f:
            f.write("\nexec \"bk_autoexec.cfg\"")


def create_bk_autoexec():
    with open(path + "/tf/cfg/bk_autoexec.cfg", "w", encoding="utf-8") as f:
        f.write("bind \"" + tf2_query_keybind + "\" \"exec bk_query.cfg\"\n")
        f.write("bind \"" + tf2_execute_keybind + "\" \"exec bk_execute.cfg\"\n")
        f.write("con_logfile console.log")


def create_bk_query():
    with open(path + "/tf/cfg/bk_query.cfg", "w", encoding="utf-8") as f:
        f.write("status")

def commid_to_usteamid(commid):
    usteamid = []
    usteamid.append('[U:1:')
    steamidacct = int(commid) - 76561197960265728

    usteamid.append(str(steamidacct) + ']')

    return ''.join(usteamid)

def get_bots():
    global botnames
    global botregexnames
    global botsteamids
    global online_database

    files = list()
    online_tf2db = list()
    if online_database:
        files.append(requests.get("https://raw.githubusercontent.com/boyonkgit/tf2-bot-kicker/main/bots.properties").text.split("\n"))
        online_tf2db = requests.get("https://tf2bdd.pazer.us/v1/steamids").json()["players"]
        b = list()
        for p in online_tf2db:
            b.append(f"steamid={commid_to_usteamid(p['steamid'])}")
        files.append(b)
    with open("bots.properties", "r",encoding="utf-8") as f:
        files.append(f.readlines())
    for file in files:
        for line in file:
            if not line.startswith("#") and not line.strip() == "":
                splitter = line.find("=")
                key = line[:splitter]
                value = line[splitter+1:].replace("\n","")
                if key == "name":
                    botnames.append(value)
                elif key == "steamid":
                    botsteamids.append(value)
                elif key == "regexname":
                    botregexnames.append(re.compile(value))
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


### ---------------- ###

### tick ----------- ###
def tick():
    query()
    sleep(1)
    get_console()
    read_console()
    detect()
    execute()


def query():
    keyboard.send(query_keybind)


def get_console():
    global raw_console
    with open(path + "/tf/console.log", "r", encoding="utf-8", errors="ignore") as f:
        raw_console = f.readlines()
    with open(path + "/tf/console.log", "w", encoding="utf-8", errors="ignore") as f:
        f.close()


def read_console():
    global raw_console
    userids = list()
    new_players = list()
    for line in raw_console:
        print(line)
        if line.startswith("#") and not line.startswith("# userid"):
            arguments = list()
            for part in line.rstrip().split(" "):
                if len(part) > 0:
                    arguments.append(part)
            if not arguments[len(arguments)-2] == "BOT":
                userid = arguments[1]
                if not userid in userids:
                    userids.append(userid)
                    original_name = line[line.find("\"")+1:line.rfind("\"")]
                    name = ""
                    for c in original_name:
                        if c.lower() in chars:
                            name = name + c.lower()
                    time = time_to_int(arguments[len(arguments)-4])
                    steamid = arguments[len(arguments)-5]
                    new_players.append(PlayerInstance(userid,name,time,steamid))
        if len(new_players) > 0:
            global players
            players = new_players

def detect():
    global players
    global clear_log
    checked_names = list()
    # if clear_log:
    #     os.system("clear")
    for player in players:
        if output_player:
            print(str(player))
        if player.name in botnames:
            votekick(player)
        elif player.steamid in botsteamids:
            votekick(player)
        elif player.name in checked_names:
            votekick(get_newest(player.name))
        else:
            for regex in botregexnames:
                if regex.match(player.name):
                    votekick(player)
        checked_names.append(player.name)

def votekick(player):
    global commands
    if output_votekick:
        print("Votekicking " + str(player))
    commands.append("callvote kick " + str(player.userid))

def execute():
    if len(commands) > 0:
        create_bk_execute()
        sleep(1)
        keyboard.send(execute_keybind)


def create_bk_execute():
    global commands
    with open(path + "/tf/cfg/bk_execute.cfg", "w", encoding="utf-8") as f:
        for command in commands:
            f.write(command + "\n")
    commands = list()

### ---------------- ###

class UI(Widget):
    def setup(self):
        teamredlabels = list()
        teambluelabels = list()

        layout = GridLayout(cols=2, row_default_height=40, pos=(0,0), size=(500,500))

        for i in range(24):
            if i%2 == 0:
                l = Label(text="red")
                teamredlabels.append(l)
            else:
                l = Label(text="blue")
                teamredlabels.append(l)
            layout.add_widget(l)

        self.add_widget(layout)


    def update(self, dt):
        tick()
        global players
        for player in players:
            pass

class UIManager(App):

    def build(self):
        self.ui = UI(pos=(100,100), size=(500,500))
        self.ui.setup()

        setup()

        Window.size = (1248, 500)
        Window.clearcolor = (0.22, 0.22, 0.22, 1)
        Window.bind(on_request_close=self.on_request_close)

        Clock.schedule_interval(self.ui.update, sleep_time)
        return self.ui

    def on_request_close(self, *args):
        os._exit(1)
        return True

### run ----------- ###
# def run():
#     setup()
#     while True:
#         sleep(sleep_time)
#         tick()
#
#
# run()

if __name__ == '__main__':
    UIManager().run()
