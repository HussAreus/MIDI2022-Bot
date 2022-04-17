import json

styles = ["red", "blue", "old"]


def register(uid):
    with open("participants.json", "r+") as f:
        data = json.load(f)
        if uid not in data.keys():
            data.update({uid: None})
            f.seek(0)
            f.truncate()
            json.dump(data, f)
            return True
        else:
            return False


"""**********************************************************
                   GUILD AND ACCOUNT STUFF
   **********************************************************"""


class Guild:
    def __init__(self, uid, name="none", points=0, channelid=None, qtokens=None, mtokens=None, style="red"):
        self.members = uid
        self.name = name
        self.points = points
        self.channelid = channelid
        self.questTokens = qtokens
        self.mapTokens = mtokens
        self.style = style

    def __repr__(self):
        string = "**_" + self.name + "_**\n"
        for member in self.members:
            string += "<@" + str(member) + ">\n"
        string += "Total Guild Points: " + str(self.points)
        string += "\nMaps unlocked:\n"
        for token in self.mapTokens:
            string += str(token) + "\n"
        return string

    def new_member(self, uid):
        if len(self.members) < 5:
            self.members.append(uid)
            return True
        else:
            return False

    def add_points(self, value, qtoken):
        if qtoken:
            if self.questTokens[qtoken]:
                return None
        self.points += value
        with open("guildlist.json", "r+") as f:
            data = json.load(f)
            data[self.name] += value
            f.seek(0)
            f.truncate()
            json.dump(data, f)

    def add_qtoken(self, token):
        if self.questTokens:
            if token not in self.questTokens.keys():
                self.questTokens.update({token: False})
                return True
            else:
                return False
        else:
            self.questTokens = {token: False}
            return True

    def set_style(self, choice):
        if choice in styles:
            self.style = choice
            return True
        else:
            return False


def create_guild(guildname, uid, channelid):
    with open("guildlist.json", "r+") as ff:
        data = json.load(ff)
        if guildname not in data.keys():
            with open("guilds/" + guildname.lower() + ".json", "w+") as f:
                json.dump(Guild(name=guildname, uid=[uid], channelid=channelid).__dict__, f)
            data.update({guildname: 0})
            # set_guild(uid, guildname)
            ff.seek(0)
            ff.truncate()
            json.dump(data, ff)
            set_guild(uid, guildname.lower())
            return True
        else:
            return False


def load_guild(guildname):
    with open("guilds/" + guildname.lower() + ".json", "r") as f:
        lst = json.load(f).values()
        data = Guild(*lst)
        return data


def upload_guild(guild):
    with open("guilds/" + guild.name.lower() + ".json", "r+") as f:
        data = guild.__dict__
        f.seek(0)
        f.truncate()
        json.dump(data, f)


def join(uid, guildname):
    try:
        guild = load_guild(guildname)
        if not guild:
            return False
        memb = guild.new_member(uid)
        if memb:
            set_guild(uid, guildname)
            upload_guild(guild)
        return True, memb
    except Exception as e:
        print(str(e) + " while joining guild")
        return False, True


def find_user(uid):
    with open("participants.json", "r") as f:
        data = json.load(f)
        if uid in data:
            return data[uid]
        else:
            return None


def set_guild(uid, guildname):
    with open("participants.json", "r+") as f:
        data = json.load(f)
        if guildname:
            data[uid] = guildname.lower()
        else:
            data[uid] = None
        f.seek(0)
        f.truncate()
        json.dump(data, f)


def update_leaderboard():
    with open("guildlist.json", "r") as f:
        print("DOING SOMETHING")
        data = json.load(f)
        sort_orders = sorted(data.items(), key=lambda x: x[1])
        for i in sort_orders:
            print(i[0], i[1])
