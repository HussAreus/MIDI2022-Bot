import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
import os

from . import botconfig
from utils.utils import glitch
import utils.QRScanner as decoder
import commands.mapCommands as mapCommands
import commands.questCommands as questCommands
import commands.guildCommands as guildCommands

"""
Requires (pip install <module>):
discord
opencv-python
pyzbar
https://github.com/Pycord-Development/pycord
"""

start = False
command_list = ["answ", "map", "maps", "quest", "quests",
                "style", "buy", "hint", "leaderboard", "lead", "rank"]


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="",
            intents=discord.Intents.all(),
        )


bot = Bot()
load_dotenv()
TOKEN = os.getenv("TOKEN")


@bot.event
async def on_ready():
    print(glitch("Satoshi Nakamoto ready to serve"))


@bot.event
async def on_message(ctx):
    if not ctx.author.bot:
        global start
        author = ctx.author
        content = ctx.content.lower()
        channel = ctx.channel
        data = content.split(" ")
        command = data[0]
        data = data[1:]
        data = ' '.join(data)
        if channel.id == botconfig.REGISTER_CHANNEL:
            if guildCommands.register(str(author.id)):
                role = get(ctx.guild.roles, id=botconfig.PARTICIPANT_ROLE)
                await author.add_roles(role)
            await ctx.delete()
        elif channel.id == botconfig.LOG_CHANNEL and command == "start":
            start = True
            await channel.send("MIDI 2022 STARTED")
        elif channel.id == botconfig.GUILD_CREATION_CHANNEL and command == "create":
            if data:
                if not guildCommands.get_user_guildname(str(author.id)):
                    if await guildCommands.create_guild(ctx, data, start):
                        await channel.send(glitch("Guild creation successful"))
                    else:
                        await channel.send(glitch("Guild creation") + " unsuccessful")
                else:
                    await channel.send(glitch("You are already in a party. Leaving a party is prohibited"))
            else:
                await channel.send(glitch("You forgot the guild name. ") + "Command is \"create <party_name>\"")
        elif channel.id == botconfig.GUILD_CREATION_CHANNEL and command == "join":
            if data:
                if not guildCommands.get_user_guildname(str(author.id)):
                    result, memb = guildCommands.join(str(author.id), data)
                    if result and memb:
                        role = get(ctx.guild.roles, name=data.lower())
                        if role:
                            await author.add_roles(role)
                        await channel.send(glitch("Joined the guild successfully"))
                    elif result:
                        await channel.send(glitch("Guild is full"))
                else:
                    await channel.send(glitch("You are already in a party. Leaving a party is prohibited"))
            else:
                await channel.send(glitch("You forgot the party name.") + "Command is \"join <partyname>\"")
        elif not start and command in command_list:
            await channel.send("Event haven't started yet")
        elif channel.id == botconfig.HELP_CHANNEL and command == "points":
            try:
                if data:
                    guildname = content.split(" ")[1]
                    points = int(content.split(" ")[2])
                    guild = guildCommands.load_guild(guildname.lower())
                    guild.add_points(points, None)
                    guildCommands.upload_guild(guild)
            except Exception as e:
                print("main" + str(e))
                await channel.send("points <guildname> <number>")
        elif command == "answ":
            result = questCommands.check_answer(str(author.id), data)
            if result:
                await channel.send(result)
        elif command == "map" or command == "maps":
            if data:
                if data.startswith("vilnius"):
                    embed = discord.Embed(
                        title="Vilnius", description="answ explorer")
                    embed.set_image(
                        url="https://media.discordapp.net/attachments/960152417687732245/966998921442381864/RedMap.png?width=1602&height=676")
                    await channel.send(embed=embed)
                else:
                    result = mapCommands.load_map(str(author.id), data)
                    if result:
                        await channel.send(embed=result)
                    else:
                        await channel.send(glitch("Unidentified map.obj for MX Matrix v1.22474487139\nAre you sure there is a map with such name?"))
            else:
                await channel.send(embed=mapCommands.load_all(str(author.id)))
        elif command == "quest" or command == "quests":
            guild = guildCommands.get_user_guild(str(author.id))
            data = " ".join(ctx.content.split(" ")[1:])
            if data:
                if data.isdigit() and 0 < int(data) < len(guild.questTokens):
                    await channel.send(embed=questCommands.load_quest(list(guild.questTokens.keys())[int(data)-1], False))
                else:
                    result = questCommands.get_quest(str(author.id), data)
                    if result:
                        await channel.send(embed=result)
            else:
                result = guild.all_quests()
                if not result:
                    result = discord.Embed(
                        title="You don't have a single quest", description="No bitches?")
                    result.set_image(
                        url="https://media.discordapp.net/attachments/826521563113324595/966071987032162424/unknown.png?width=623&height=670")
                await channel.send(embed=result)
        elif command == "style":
            if data:
                guild = guildCommands.get_user_guild(str(author.id))
                result = guild.set_style(data)
                if result:
                    guildCommands.upload_guild(guild)
                    await channel.send(glitch("Interface style changed to \""+data+"\""))
                else:
                    await channel.send(glitch("No such style in databases"))
        elif command == "buy":
            embed = mapCommands.buy_map(str(author.id), data)
            if embed:
                await channel.send(embed=embed)
        elif command == "hint":
            sub_channel = get(ctx.guild.channels, id=botconfig.HELP_CHANNEL)
            await sub_channel.send("<@&945782392596074526> Help request at <#" + str(channel.id) + ">")
        elif command == "leaderboard" or command == "lead" or command == "rank":
            if channel.id == botconfig.LOG_CHANNEL:
                result = guildCommands.update_leaderboard()
                if result:
                    await channel.send(glitch(result))
            else:
                guild = guildCommands.get_user_guild(str(author.id))
                await channel.send(embed=guild.lead())
        elif start and len(ctx.attachments) > 0:
            for file in ctx.attachments:
                sub_channel = get(ctx.guild.channels, id=botconfig.LOG_CHANNEL)
                if file.filename.lower().endswith(".png") or file.filename.lower().endswith(".jpg") or file.filename.lower().endswith(".jpeg"):
                    text = decoder.decode_qr(file)
                    if text:
                        text = text.split(" ")
                        command = text[0]
                        text = ' '.join(text[1:])
                        if command == "quest" and text:
                            result = questCommands.get_quest(
                                str(author.id), text)
                            if result:
                                await channel.send(embed=result)
                            else:
                                await sub_channel.send("Unexpected image at channel: <#" + str(channel.id) + ">")
                        elif command == "map" and text:
                            result = mapCommands.load_map(str(author.id), text)
                            if result:
                                await channel.send(embed=result)
                            else:
                                await sub_channel.send("Unexpected image at channel: <#" + str(channel.id) + ">")
                        elif text:
                            await channel.send(command + " " + text)
                            await sub_channel.send("Unexpected image at channel: <#" + str(channel.id) + ">")
                    else:
                        await sub_channel.send("Unexpected image at channel: <#" + str(channel.id) + ">")
                else:
                    await sub_channel.send("Unexpected attachment at channel: <#" + str(channel.id) + ">")


bot.run(TOKEN)
