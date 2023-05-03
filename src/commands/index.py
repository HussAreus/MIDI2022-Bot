import discord
from discord.utils import get

from bot import botconfig
import commands.guildCommands as guildCommands
import commands.questCommands as questCommands
import commands.mapCommands as mapCommands
from utils.utils import glitch
import utils.QRScanner as scanner


class CommandList:
    __slots__ = ()
    CREATE = ["create"]
    JOIN = ["join"]
    POINTS = ["points"]
    ANSW = ["answ", "answer"]
    MAP = ["map", "maps"]
    QUEST = ["quest", "quests"]
    STYLE = ["style"]
    BUY = ["buy", "purchase"]
    HINT = ["hint", "clue"]
    LEADERBOARD = ["leaderboard", "lead", "rank"]

    def has_command(self, command):
        try:
            for attr in dir(self):
                if command in getattr(self, attr):
                    return True
            return False
        except:
            return False


command_list = CommandList()


async def command(ctx, start):
    """ Checks if the message is a command """
    content = ctx.content.lower()
    channel = ctx.channel
    command = content.split(" ")[0]
    args = content.replace(command, "").strip()

    if channel.id == botconfig.REGISTER_CHANNEL:
        await register(ctx)
    elif channel.id == botconfig.GUILD_CREATION_CHANNEL:
        if command in command_list.CREATE:
            await create(ctx, args, start)
        elif command in command_list.JOIN:
            await join(ctx, args)
    elif channel.id == botconfig.HELP_CHANNEL:
        if command in command_list.POINTS:
            points = args.split(" ")[-1]
            guildname = args.replace(points, "").strip()
            points(ctx, guildname, points)
    elif channel.id not in botconfig.PUBLIC_CHANNELS:
        if command_list.has_command(command) and not start:
            await ctx.channel.send(glitch("MIDI 2022 has not started yet"))
        elif command in command_list.ANSW:
            await answer(ctx, args)
        elif command in command_list.MAP:
            await map(ctx, args)
        elif command in command_list.QUEST:
            await quest(ctx, args)
        elif command in command_list.STYLE:
            await style(ctx, args)
        elif command in command_list.BUY:
            await buy(ctx, args)
        elif command in command_list.HINT:
            await hint(ctx, args)
        elif command in command_list.LEADERBOARD:
            await leaderboard(ctx, args)
        elif len(ctx.attachments) > 0:
            await scan(ctx)


async def register(ctx):
    if guildCommands.register(str(ctx.author.id)):
        role = get(ctx.guild.roles, id=botconfig.PARTICIPANT_ROLE)
        await ctx.author.add_roles(role)
    await ctx.delete()


async def create(ctx, guildname, start):
    if not guildname:
        await ctx.channel.send(glitch("You forgot the guild name. ") + "Command is \"create <guild_name>\"")
        return
    if guildCommands.get_user_guildname(str(ctx.author.id)):
        await ctx.channel.send(glitch("You are already in a guild. Leaving a guild is prohibited"))
        return

    if await guildCommands.create_guild(ctx, guildname, start):
        await ctx.channel.send(glitch("Guild creation successful"))
    else:
        await ctx.channel.send(glitch("Guild creation") + " unsuccessful")


async def join(ctx, guildname):
    if not guildname:
        await ctx.channel.send(glitch("You forgot the guild name.") + "Command is \"join <guild_name>\"")
        return
    if guildCommands.get_user_guildname(str(ctx.author.id)):
        await ctx.channel.send(glitch("You are already in a guild. Leaving a guild is prohibited"))
        return

    result, memb = guildCommands.join(str(ctx.author.id), guildname)
    if result and memb:
        role = get(ctx.guild.roles, name=guildname.lower())
        if role:
            await ctx.author.add_roles(role)
        await ctx.channel.send(glitch("Joined the guild successfully"))
    elif result:
        await ctx.channel.send(glitch("Guild is full"))


async def points(ctx, guildname, points):
    try:
        if guildname and points:
            guild = guildCommands.load_guild(guildname.lower())
            guild.add_points(points, None)
            guildCommands.upload_guild(guild)
    except Exception as e:
        print("main" + str(e))
        await ctx.channel.send("points <guildname> <number>")


async def answer(ctx, answer):
    result = questCommands.check_answer(str(ctx.author.id), answer)
    if result:
        await ctx.channel.send(result)


async def map(ctx, mapname):
    if not mapname:
        await ctx.channel.send(embed=mapCommands.load_all(str(ctx.author.id)))
        return

    # Easter egg
    if mapname.startswith("vilnius"):
        embed = discord.Embed(
            title="Vilnius", description="answ explorer")
        embed.set_image(
            url="https://media.discordapp.net/attachments/960152417687732245/966998921442381864/RedMap.png?width=1602&height=676")
        await ctx.channel.send(embed=embed)
        return

    result = mapCommands.load_map(str(ctx.author.id), mapname)
    if result:
        await ctx.channel.send(embed=result)
    else:
        await ctx.channel.send(glitch("Unidentified map.obj for MX Matrix v1.22474487139\nAre you sure there is a map with such name?"))


async def quest(ctx, questname):
    guild = guildCommands.get_user_guild(str(ctx.author.id))
    if questname:
        if questname.isdigit() and 0 < int(questname) < len(guild.questTokens):
            result = questCommands.load_quest(
                list(guild.questTokens.keys())[int(questname)-1], False)
        else:
            result = questCommands.get_quest(str(ctx.author.id), questname)
    else:
        result = guild.all_quests()
        if not result:
            result = discord.Embed(
                title="You don't have a single quest", description="No bitches?")
            result.set_image(
                url="https://media.discordapp.net/attachments/826521563113324595/966071987032162424/unknown.png?width=623&height=670")

    if result:
        await ctx.channel.send(embed=result)


async def style(ctx, stylename):
    if not stylename:
        await ctx.channel.send(glitch("No such style in databases"))
        return

    guild = guildCommands.get_user_guild(str(ctx.author.id))
    result = guild.set_style(stylename)
    if result:
        guildCommands.upload_guild(guild)
        await ctx.channel.send(glitch("Interface style changed to \""+stylename+"\""))


async def buy(ctx, mapID):
    embed = mapCommands.buy_map(str(ctx.author.id), mapID)
    if embed:
        await ctx.channel.send(embed=embed)


async def hint(ctx):
    help_channel = get(ctx.guild.channels, id=botconfig.HELP_CHANNEL)
    await help_channel.send("<@&{}> Help request at <#".format(botconfig.ADMIN_ID) + str(ctx.channel.id) + ">")


async def leaderboard(ctx):
    if ctx.channel.id == botconfig.LOG_CHANNEL:
        result = guildCommands.update_leaderboard()
        if result:
            await ctx.channel.send(glitch(result))
    else:
        guild = guildCommands.get_user_guild(str(ctx.author.id))
        await ctx.channel.send(embed=guild.leaderboard())


async def scan(ctx):
    log_channel = get(ctx.guild.channels, id=botconfig.LOG_CHANNEL)
    for file in ctx.attachments:
        if not (file.filename.lower().endswith(".png") or file.filename.lower().endswith(".jpg") or file.filename.lower().endswith(".jpeg")):
            await log_channel.send("Unexpected file at channel: <#" + str(ctx.channel.id) + ">")
            return

        text = scanner.decode_qr(file)
        if not text:
            await log_channel.send("Unexpected image at channel: <#" + str(ctx.channel.id) + ">")
            return

        command = text.split(" ")[0]
        args = text.replace(command, "").strip()
        if not args:
            return

        if command in command_list.QUEST:
            result = questCommands.get_quest(str(ctx.author.id), args)
        elif command == "map" and text:
            result = mapCommands.load_map(str(ctx.author.id), text)
        elif text:
            result = discord.Embed(title=command + " " + text)

        if result:
            await ctx.channel.send(embed=result)
        else:
            await log_channel.send("Unexpected image at channel: <#" + str(ctx.channel.id) + ">")
