import discord
from discord.ext import commands
from discord.commands import Option
from dotenv import load_dotenv
import os

bot = commands.Bot(command_prefix="")
load_dotenv()
TOKEN = os.getenv("TOKEN2")


@bot.event
async def on_ready():
    print("Help bot ready")


@bot.event
async def on_message(ctx):
    if not ctx.author.bot:
        author = ctx.author
        content = ctx.content.lower()
        channel = ctx.channel

        data = content.split(" ")
        command = data[0]
        data = data[1:]
        data = ' '.join(data)


@bot.slash_command(guild_ids=[928239290440372295], description="No idea")
async def help(ctx, command: Option(str, "Choose command [Default: All]", choices=["all", "commands", "start", "end", "maps", "quest", "answ", "buy", "hint", "leaderboard", "style"], default="All", required=False)):
    command = command.lower()
    if command == "all":
        embed = discord.Embed(title="Things I can help with:")
        embed.add_field(name="/help commands", value="A full list of commands", inline=False)
        embed.add_field(name="/help start", value="A quick introduction to the gameplay", inline=False)
        embed.add_field(name="/help end", value="A review of what will happen when the game ends", inline=False)
        await ctx.respond(embed=embed)
    elif command == "commands":
        embed = discord.Embed(title="Here is a list of \"all\" commands")
        embed.add_field(name="maps", value="A command used for accessing maps", inline=False)
        embed.add_field(name="quests", value="A command used for accessing quests", inline=False)
        embed.add_field(name="answ", value="A command used when you want to provide an answer to a quest", inline=False)
        embed.add_field(name="buy", value="A command used for purchasing a map", inline=False)
        embed.add_field(name="hint", value="A command for those who got stuck", inline=False)
        embed.add_field(name="leaderboard", value="Let's get competitive", inline=False)
        await ctx.respond(embed=embed)
    elif command == "maps":
        embed = discord.Embed(title="Command map/maps")
        embed.add_field(name="By default", value="Provides a full list of unlocked and not unlocked maps", inline=False)
        embed.add_field(name="maps <map_name>. (Example: maps Lietuva)", value="Loads a speciffic map with its' objectives", inline=False)
        embed.set_footer(text="You can unlock a new map with this same command. Just use maps<map_name>\nEach new map gives you points")
        await ctx.respond(embed=embed)
    elif command == "quests":
        embed = discord.Embed(title="Command quest/quests")
        embed.add_field(name="By default", value="Provides a full list of unlocked quests", inline=False)
        embed.add_field(name="quests <quest_ID>. (Example: quests abrakadabra)", value="Loads a speciffic quest based on index. You can see those indices when you use default command \"quests\"", inline=False)
        embed.set_footer(text="To unlock a quest simply send a photo of a QR code to the private party channel.\nIf bot cannot read it properly either try again, or read it with another program and simply type in what that QR code hides\nEach new quest gives you points")
        await ctx.respond(embed=embed)
    elif command == "answ":
        embed = discord.Embed(title="Command answ")
        embed.add_field(name="answ <quest_answer>", value="Just shoot the answer. If it is correct, you will get points.", inline=False)
        await ctx.respond(embed=embed)

bot.run(TOKEN)