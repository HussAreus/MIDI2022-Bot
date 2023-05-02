import discord
import random
import json
from discord.utils import get
from datetime import datetime

from . import mapCommands
from utils.Guild import Guild
import bot.botconfig as botconfig


"""
*************************************************************
				   GUILD RELATED COMMANDS
*************************************************************
create_guild       - creates a new guild and displays a map
load_guild         - loads a guild from its own separate file
upload_guild       - uploads a guild to its own separate file
join               - adds new member to a guild
leave              - removes a member from a guild
get_user_guildname - gets a user's guild name from participants file
set_user_guildname - sets a user's guild name in participants file
get_user_guild     - gets a user's guild
register           - registers a user as a participant. Gives role so they can see channels
update_leaderboard - updates the leaderboard
************************************************************
"""


async def create_guild(ctx, guildname: str, start: bool):
    """ Creates a new guild and displays a map """
    guild = ctx.guild
    member = ctx.author
    guildrole = await guild.create_role(name=guildname.lower(), colour=discord.Colour(0x00FF00))
    adminrole = get(ctx.guild.roles, id=botconfig.ADMIN_ROLE)
    await member.add_roles(guildrole)
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guildrole: discord.PermissionOverwrite(read_messages=True),
        adminrole: discord.PermissionOverwrite(read_messages=True)
    }
    channel = await guild.create_text_channel(guildname, overwrites=overwrites)
    new_guild(guildname, str(member.id), channel.id)

    # THIS WILL BE VISIBLE ON DISCORD:
    chosen = random.choice(["Mobil Avenue", "Zion", "Mega City", "Backdoor"])
    if start:
        await channel.send("Free map: " + chosen + "\nyou can re-open it using \"map <map_name>\" command")
    else:
        if chosen.lower() == "mobil avenue":
            await channel.send("**Free map: " + chosen + ". Organizers will be waiting by the Gates of Dawn**")
        elif chosen.lower() == "backdoor":
            await channel.send("**Free map: " + chosen + ". Organizers will be waiting by the MO Museum (Pylimo str. 17)**")
        elif chosen.lower() == "mega city":
            await channel.send("**Free map: " + chosen + ". Organizers will be waiting by the Town Hall Square**")
        elif chosen.lower() == "zion":
            await channel.send("**Free map: " + chosen + ". Organizers will be waiting by the Tymo Bazaar**")

    mapCommands.load_map(str(member.id), chosen.lower())
    embed = mapCommands.load_all(str(member.id))
    embed.set_footer(text="You can access this menu by using command \"map\"")
    await channel.send(embed=embed)
    return True


def new_guild(guildname: str, leaderUID: int, channelid: int):
    """ Creates a new guild and saves it to guildlist file and its own separate file """
    with open(botconfig.GUILDLIST_PATH, "r+") as ff:
        data = json.load(ff)
        if guildname not in data:
            with open("guilds/" + guildname.lower() + ".json", "w+") as f:
                json.dump(Guild(leaderUID, guildname, channelid).__dict__, f)
            data[guildname] = 0
            ff.seek(0)
            ff.truncate()
            json.dump(data, ff)
            set_user_guildname(leaderUID, guildname.lower())
            return True
        else:
            return False


def load_guild(guildname: str):
    """ Loads a guild from its own separate file """
    with open('resources/guilds/' + guildname.lower() + ".json", "r") as f:
        lst = json.load(f).values()
        return Guild(*lst)


def upload_guild(guild: Guild):
    """ Uploads a guild to its own separate file """
    with open('resources/guilds/' + guild.name.lower() + ".json", "r+") as f:
        data = guild.__dict__
        f.seek(0)
        f.truncate()
        json.dump(data, f)


def join(uid: int, guildname: str):
    """ Adds new member to a guild """
    try:
        guild = load_guild(guildname)
        if not guild:
            return False
        join_success = guild.new_member(uid)
        if join_success:
            set_user_guildname(uid, guildname)
            upload_guild(guild)
        return True, join_success
    except Exception as e:
        print(str(e) + " while joining guild")
        return False, True


def register(uid: int):
    with open(botconfig.PARTICIPANTS_PATH, "r+") as f:
        data = json.load(f)
        if uid not in data.keys():
            data.update({uid: None})
            f.seek(0)
            f.truncate()
            json.dump(data, f)
            return True
        else:
            return False


def get_user_guildname(uid: int):
    """ Returns a user's guild name """
    with open(botconfig.PARTICIPANTS_PATH, "r") as f:
        data = json.load(f)
        if uid in data:
            return data[uid]
        else:
            return None


def set_user_guildname(uid: int, guildname: str):
    """ Sets a user's guild name """
    with open(botconfig.PARTICIPANTS_PATH, "r+") as f:
        data = json.load(f)
        if guildname:
            data[uid] = guildname.lower()
        else:
            data[uid] = None
        f.seek(0)
        f.truncate()
        json.dump(data, f)


def get_user_guild(uid: int):
    """ Returns a user's guild """
    guildname = get_user_guildname(uid)
    return load_guild(guildname)


# Really dumb way to do this. TODO: make it better
last_update = "00:00"


def update_leaderboard():
    """ Generates a new leaderboard. Each guild is mapped to 4 other guilds (based on points) """
    with open(botconfig.GUILDLIST_PATH, "r") as f:
        data = json.load(f)
    sorted_data = sorted(data.items(), key=lambda x: x[1])
    with open(botconfig.LEADERBOARD_PATH, "w") as ff:
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

    # Update last update time and return the top 10 guilds
    now = datetime.now()
    global last_update
    last_update = now.strftime("%H:%M")
    result = ""
    if end > 10:
        end = 10
    for i in range(1, end+1):
        result += "No." + \
            str(i) + " " + sorted_data[end-i][0] + \
            " " + str(sorted_data[end-i][1]) + "\n"
    return result
