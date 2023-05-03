import discord
from discord.ext import commands
from discord.utils import get
from discord.commands import Option
from dotenv import load_dotenv
import os

from . import botconfig
from utils.utils import glitch
from commands.index import command
import commands.guildCommands as guildCommands

start = False


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
        if ctx.channel.id == botconfig.LOG_CHANNEL and ctx.content.lower() == "start":
            start = True
            await ctx.channel.send("MIDI 2022 STARTED")
        else:
            await command(ctx, start)


def isGuildCreationChannel(ctx):
    """Checks if the current channel is the guild creation channel"""
    return ctx.channel.id == botconfig.GUILD_CREATION_CHANNEL


@ bot.slash_command(guild_ids=[botconfig.SERVER_ID], description="Create your guild", checks=[isGuildCreationChannel])
async def create(ctx, guild_name: Option(str, "Choose guild name", required=True)):
    """ Slash command for guild creation """
    author = ctx.author
    channel = ctx.channel
    if not channel.id == botconfig.GUILD_CREATION_CHANNEL:
        await ctx.respond("<#{}> Only".format(botconfig.GUILD_CREATION_CHANNEL), ephemeral=True)
        return
    if not guild_name:
        await ctx.respond(glitch("You forgot the guild name. ") + "Command is \"create <guild_name>\"", ephemeral=True)
        return
    if guildCommands.find_user(str(author.id)):
        await ctx.respond(glitch("You are already in a guild. The organisators prohibited leaving a guild"), ephemeral=True)

    if await guildCommands.new_guild(ctx, guild_name):
        await ctx.respond(glitch("Guild creation successful"), ephemeral=True)
    else:
        await ctx.respond(glitch("Guild creation") + " unsuccessful", ephemeral=True)


@ bot.slash_command(guild_ids=[botconfig.SERVER_ID], description="Join a guild", checks=[isGuildCreationChannel])
async def join(ctx, guild_name: Option(str, "Choose guild name", required=True)):
    """ Slash command for joining a guild """
    author = ctx.author
    channel = ctx.channel
    if not channel.id == botconfig.GUILD_CREATION_CHANNEL:
        await ctx.respond("<#{}> Only".format(botconfig.GUILD_CREATION_CHANNEL), ephemeral=True)
        return
    if not guild_name:
        await ctx.respond(glitch("You forgot the guild name.") + "Command is \"join <guild_name>\"", ephemeral=True)
        return
    if guildCommands.find_guild(guild_name):
        await ctx.respond(glitch("You are already in a guild"), ephemeral=True)
        return

    result, memb = guildCommands.join(str(author.id), guild_name)
    if result and memb:
        role = get(ctx.guild.roles, name=guild_name.lower())
        if role:
            await author.add_roles(role)
        await ctx.respond(glitch("Joined the guild successfully"), ephemeral=True)
    elif result:
        await ctx.respond(glitch("Guild is full"), ephemeral=True)


bot.run(TOKEN)
