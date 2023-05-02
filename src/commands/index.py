from discord.commands import Option
from discord.ext import commands
from discord.utils import get

from bot import botconfig
from bot.main import bot
import commands.guildCommands as guildCommands
from utils.utils import glitch


def command(ctx, *args):
    pass


def isGuildCreationChannel(ctx):
    """Checks if the current channel is the guild creation channel"""
    return ctx.channel.id == botconfig.GUILD_CREATION_CHANNEL


@bot.slash_command(guild_ids=[botconfig.SERVER_ID], description="Create your guild", checks=[isGuildCreationChannel])
async def create(ctx, guild_name: Option(str, "Choose guild name", required=True)):
    """ Slash command for guild creation """
    author = ctx.author
    channel = ctx.channel
    if channel.id == botconfig.GUILD_CREATION_CHANNEL:
        if guild_name:
            if not guildCommands.find_user(str(author.id)):
                if await guildCommands.new_guild(ctx, guild_name):
                    await ctx.respond(glitch("Guild creation successful"), ephemeral=True)
                else:
                    await ctx.respond(glitch("Guild creation") + " unsuccessful", ephemeral=True)
            else:
                await ctx.respond(glitch("You are already in a guild. The organisators prohibited leaving a guild"), ephemeral=True)
        else:
            await ctx.respond(glitch("You forgot the guild name. ") + "Command is \"create <guild_name>\"", ephemeral=True)
    else:
        await ctx.respond("<#{}> Only".format(botconfig.GUILD_CREATION_CHANNEL), ephemeral=True)


@bot.slash_command(guild_ids=[botconfig.SERVER_ID], description="Join a guild", checks=[isGuildCreationChannel])
async def join(ctx, guild_name: Option(str, "Choose guild name", required=True)):
    """ Slash command for joining a guild """
    author = ctx.author
    channel = ctx.channel
    if channel.id == botconfig.GUILD_CREATION_CHANNEL:
        if guild_name:
            if not guildCommands.find_user(str(author.id)):
                result, memb = guildCommands.join(str(author.id), guild_name)
                if result and memb:
                    role = get(ctx.guild.roles, name=guild_name.lower())
                    if role:
                        await author.add_roles(role)
                    await ctx.respond(glitch("Joined the guild successfully"), ephemeral=True)
                elif result:
                    await ctx.respond(glitch("Guild is full"), ephemeral=True)
            else:
                await ctx.respond(glitch("You are already in a guild"), ephemeral=True)
        else:
            await ctx.respond(glitch("You forgot the guild name.") + "Command is \"join <guild_name>\"", ephemeral=True)
    else:
        await ctx.respond("<#{}> Only".format(botconfig.GUILD_CREATION_CHANNEL), ephemeral=True)
