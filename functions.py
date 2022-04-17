import json
import discord
from datetime import datetime


styles = ["red", "blue", "old"]
last_update = "00:00"


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

    def lead(self):
        try:
            with open("leaderboard.json", "r") as f:
                data = json.load(f)[self.name.lower()]
                embed = discord.Embed(title="Latest leaderboards:")
                for i in range(0, len(data)):
                    embed.add_field(name=data[-i][0], value="Points collected: " + str(data[-i][1]), inline=False)
                embed.set_footer(text="Last update "+last_update)
                return embed
        except Exception as e:
            print(e)
            return discord.Embed(title="Leaderboard is not prepared yet. Try again later", description="We update leaderboards every 30 minutes")


def create_guild(guildname, uid, channelid):
    with open("guildlist.json", "r+") as ff:
        data = json.load(ff)
        if guildname not in data.keys():
            with open("guilds/" + guildname.lower() + ".json", "w+") as f:
                json.dump(Guild(name=guildname, uid=[uid], channelid=channelid).__dict__, f)
            data.update({guildname: 0})
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
        data = json.load(f)
    sorted_data = sorted(data.items(), key=lambda x: x[1])
    with open("leaderboard.json", "w") as ff:
        new_data = {}
        end = len(sorted_data)
        for i in range(0, end):
            listas = []
            if i >= 2:
                listas.append(sorted_data[i-2])
            if i >= 1:
                listas.append(sorted_data[i-1])
            listas.append(sorted_data[i])
            if i < end-1:
                listas.append(sorted_data[i+1])
            if i < end-2:
                listas.append(sorted_data[i+2])
            new_data[sorted_data[i][0]] = listas
        json.dump(new_data, ff)

    now = datetime.now()
    global last_update
    last_update = now.strftime("%H:%M")
    result = ""
    if end > 10:
        end = 10
    for i in range(1, end+1):
        result += "No." + str(i) + " " + sorted_data[end-i][0] + " " + str(sorted_data[end-i][1]) + "\n"
    return result
