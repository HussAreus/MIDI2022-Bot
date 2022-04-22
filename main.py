import discord
from discord.ext import commands
from discord.utils import get
from discord.commands import Option
from dotenv import load_dotenv
import functions
import maps
import decode
import random
import os

"""
Requires (pip install <module>):
discord
opencv-python
pyzbar
https://github.com/Pycord-Development/pycord
"""

REGISTER_CHANNEL = 966964571027951646
ADMIN_CHANNEL = 965163235290533928
GUILD_CHANNEL = 966964399225073666
HJELP_CHANNEL = 966966877450559508
start = False
command_list = ["answ", "map", "maps", "quest", "quests", "style", "buy", "hint", "leaderboard", "lead", "rank"]


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
    print(maps.glitch("Satoshi Nakamoto ready to serve"))


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
        if channel.id == REGISTER_CHANNEL:
            if functions.register(str(author.id)):
                role = get(ctx.guild.roles, id=961558123435401286)
                await author.add_roles(role)
            await ctx.delete()
        elif channel.id == ADMIN_CHANNEL and command == "start":
            start = True
            await channel.send("MIDI 2022 STARTED")
        elif channel.id == GUILD_CHANNEL and command == "create":
            if data:
                if not functions.find_user(str(author.id)):
                    if await create_guild(ctx, data):
                        await channel.send(maps.glitch("Guild creation successful"))
                    else:
                        await channel.send(maps.glitch("Guild creation") + " unsuccessful")
                else:
                    await channel.send(maps.glitch("You are already in a party. Leaving a party is prohibited"))
            else:
                await channel.send(maps.glitch("You forgot the guild name. ") + "Command is \"create <party_name>\"")
        elif channel.id == GUILD_CHANNEL and command == "join":
            if data:
                if not functions.find_user(str(author.id)):
                    result, memb = functions.join(str(author.id), data)
                    if result and memb:
                        role = get(ctx.guild.roles, name=data.lower())
                        if role:
                            await author.add_roles(role)
                        await channel.send(maps.glitch("Joined the guild successfully"))
                    elif result:
                        await channel.send(maps.glitch("Guild is full"))
                else:
                    await channel.send(maps.glitch("You are already in a party. Leaving a party is prohibited"))
            else:
                await channel.send(maps.glitch("You forgot the party name.") + "Command is \"join <partyname>\"")
        elif not start and command in command_list:
            await channel.send("Event haven't started yet")
        elif channel.id == HJELP_CHANNEL and command == "points":
            try:
                if data:
                    guildname = content.split(" ")[1]
                    points = int(content.split(" ")[2])
                    guild = functions.load_guild(guildname.lower())
                    guild.add_points(points, None)
                    functions.upload_guild(guild)
            except Exception as e:
                print("main" + str(e))
                await channel.send("points <guildname> <number>")
        elif command == "answ":
            result = maps.check_answer(str(author.id), data)
            if result:
                await channel.send(result)
        elif command == "map" or command == "maps":
            if data:
                if data.startswith("vilnius"):
                    embed = discord.Embed(title="Vilnius", description="answ explorer")
                    embed.set_image(url="https://media.discordapp.net/attachments/960152417687732245/966998921442381864/RedMap.png?width=1602&height=676")
                    await channel.send(embed=embed)
                else:
                    result = maps.load_map(str(author.id), data)
                    if result:
                        await channel.send(embed=result)
                    else:
                        await channel.send(maps.glitch("Unidentified map.obj for MX Matrix v1.22474487139\nAre you sure there is a map with such name?"))
            else:
                await channel.send(embed=maps.load_all(str(author.id)))
        elif command == "quest" or command == "quests":
            guild = functions.load_guild(functions.find_user(str(author.id)))
            data = " ".join(ctx.content.split(" ")[1:])
            if data:
                if data.isdigit() and 0 < int(data) < len(guild.questTokens):
                    await channel.send(embed=maps.load_quest(list(guild.questTokens.keys())[int(data)-1], False))
                else:
                    result = maps.get_task(str(author.id), data)
                    if result:
                        await channel.send(embed=result)
            else:
                result = guild.all_quests()
                if not result:
                    result = discord.Embed(title="You don't have a single quest", description="No bitches?")
                    result.set_image(url="https://media.discordapp.net/attachments/826521563113324595/966071987032162424/unknown.png?width=623&height=670")
                await channel.send(embed=result)
        elif command == "style":
            if data:
                guildname = functions.find_user(str(author.id))
                guild = functions.load_guild(guildname)
                result = guild.set_style(data)
                if result:
                    functions.upload_guild(guild)
                    await channel.send(maps.glitch("Interface style changed to \""+data+"\""))
                else:
                    await channel.send(maps.glitch("No such style in databases"))
        elif command == "buy":
            embed = maps.buy_map(str(author.id), data)
            if embed:
                await channel.send(embed=embed)
        elif command == "hint":
            sub_channel = get(ctx.guild.channels, id=HJELP_CHANNEL)
            await sub_channel.send("<@&945782392596074526> Help request at <#" + str(channel.id) + ">")
        elif command == "leaderboard" or command == "lead" or command == "rank":
            if channel.id == ADMIN_CHANNEL:
                result = functions.update_leaderboard()
                if result:
                    await channel.send(maps.glitch(result))
            else:
                guildname = functions.find_user(str(author.id))
                guild = functions.load_guild(guildname)
                await channel.send(embed=guild.lead())
        elif start and len(ctx.attachments) > 0:
            for file in ctx.attachments:
                sub_channel = get(ctx.guild.channels, id=962275479564468224)
                if file.filename.lower().endswith(".png") or file.filename.lower().endswith(".jpg") or file.filename.lower().endswith(".jpeg"):
                    text = decode.decode_qr(file)
                    if text:
                        text = text.split(" ")
                        command = text[0]
                        text = ' '.join(text[1:])
                        if command == "quest" and text:
                            result = maps.get_task(str(author.id), text)
                            if result:
                                await channel.send(embed=result)
                            else:
                                await sub_channel.send("Unexpected image at channel: <#" + str(channel.id) + ">")
                        elif command == "map" and text:
                            result = maps.load_map(str(author.id), text)
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


@bot.slash_command(guild_ids=[928239290440372295], description="Create your party")
async def create(ctx, party_name: Option(str, "Choose party name", required=True)):
    author = ctx.author
    channel = ctx.channel
    if channel.id == GUILD_CHANNEL:
        if party_name:
            if not functions.find_user(str(author.id)):
                if await create_guild(ctx, party_name):
                    await ctx.respond(maps.glitch("Guild creation successful"), ephemeral=True)
                else:
                    await ctx.respond(maps.glitch("Guild creation") + " unsuccessful", ephemeral=True)
            else:
                await ctx.respond(maps.glitch("You are already in a party. The organisators prohibited leaving a party"), ephemeral=True)
        else:
            await ctx.respond(maps.glitch("You forgot the guild name. ") + "Command is \"create <party_name>\"", ephemeral=True)
    else:
        await ctx.respond("<#966964399225073666> Only")


@bot.slash_command(guild_ids=[928239290440372295], description="Join a party")
async def join(ctx, party_name: Option(str, "Choose party name", required=True)):
    author = ctx.author
    channel = ctx.channel
    if channel.id == GUILD_CHANNEL:
        if party_name:
            if not functions.find_user(str(author.id)):
                result, memb = functions.join(str(author.id), party_name)
                if result and memb:
                    role = get(ctx.guild.roles, name=party_name.lower())
                    if role:
                        await author.add_roles(role)
                    await ctx.respond(maps.glitch("Joined the guild successfully"), ephemeral=True)
                elif result:
                    await ctx.respond(maps.glitch("Guild is full"), ephemeral=True)
            else:
                await ctx.respond(maps.glitch("You are already in a party"), ephemeral=True)
        else:
            await ctx.respond(maps.glitch("You forgot the party name.") + "Command is \"join <partyname>\"", ephemeral=True)
    else:
        await ctx.respond("<#966964399225073666> Only")


async def create_guild(ctx, guildname):
    guild = ctx.guild
    member = ctx.author
    guildrole = await guild.create_role(name=guildname.lower(), colour=discord.Colour(0x00FF00))
    pagalbininkai = get(ctx.guild.roles, id=945782392596074526)
    await member.add_roles(guildrole)
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guildrole: discord.PermissionOverwrite(read_messages=True),
        pagalbininkai: discord.PermissionOverwrite(read_messages=True)
    }
    channel = await guild.create_text_channel(guildname, overwrites=overwrites)
    functions.create_guild(guildname, str(member.id), channel.id)
    # THIS WILL BE VISIBLE:

    chosen = random.choice(["Mobil Avenue", "Zion", "Mega City", "Backdoor"])
    if start:
        await channel.send("Nemokamas žemėlapis: " + chosen + "\ngali peržiūrėti jį naudodamas \"map <map_name>\" komandą")
    else:
        if chosen.lower() == "mobil avenue":
            await channel.send("**Nemokamas žemėlapis: " + chosen + ". Organizuotojai lauks prie Aušros vartų**")
        elif chosen.lower() == "backdoor":
            await channel.send("**Nemokamas žemėlapis: " + chosen + ". Organizuotojai lauks prie Pylimo g. 17 (MO muziejus)**")
        elif chosen.lower() == "mega city":
            await channel.send("**Nemokamas žemėlapis: " + chosen + ". Organizuotojai lauks Rotušės aikštėje**")
        elif chosen.lower() == "zion":
            await channel.send("**Nemokamas žemėlapis: " + chosen + ". Organizuotojai lauks prie Tymo turgaus**")

    maps.load_map(str(member.id), chosen.lower())
    embed = maps.load_all(str(member.id))
    embed.set_footer(text="You can access this menu by using command \"map\"")
    await channel.send(embed=embed)
    return True

bot.run(TOKEN)
