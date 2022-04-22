import discord
from discord.ext import commands
from discord.commands import Option
from dotenv import load_dotenv
import os
import time


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="",
            intents=discord.Intents.all(),
        )


bot = Bot()
load_dotenv()
TOKEN = os.getenv("TOKEN2")
banned_channels = [966964399225073666]


@bot.event
async def on_ready():
    print("Help bot ready")


@bot.event
async def on_message(ctx):
    if ctx.channel.id in banned_channels:
        time.sleep(3)
        await ctx.delete()


@bot.slash_command(guild_ids=[928239290440372295], description="Helps you. Perchance")
async def help(ctx, help_with: Option(str, "Choose command [Default: All]", choices=["all", "commands", "end", "maps", "quests", "answ", "buy", "hint", "leaderboard", "style"], default="All", required=False)):
    command = help_with.lower()
    if command == "all":
        embed = discord.Embed(title="Things I can help with:")
        embed.add_field(name="/help commands", value="A full list of commands", inline=False)
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
        embed.add_field(name="maps <map_name>. (Example: maps Vilnius)", value="Loads a speciffic map with its' objectives", inline=False)
        embed.set_footer(text="You can unlock a new map with this same command. Just use maps<map_name>\nEach new map gives you points")
        await ctx.respond(embed=embed)
    elif command == "quests":
        embed = discord.Embed(title="Command quest/quests")
        embed.add_field(name="By default", value="Provides a full list of unlocked quests", inline=False)
        embed.add_field(name="quests <quest_ID>. (Pvz: quests abrakadabra)", value="Užkrauna užduotį pagal indeksą. Indeksus gali matyti panaudojęs komandą \"quests\"", inline=False)
        embed.set_footer(text="Norint atrakinti užduotį siųsk į channelį QR kodo nuotrauką arba nuskaitęs jį persiųsk tekstą čia, o jau Hackeris susitvarkys\nKiekviena nauja užduotis - nauji taškai ")
        await ctx.respond(embed=embed)
    elif command == "answ":
        embed = discord.Embed(title="Komanda answ")
        embed.add_field(name="answ <quest_answer>", value="Jei atsakymas teisingas, Hackeris automatiškai išsiaiškins kuri užduotis", inline=False)
        await ctx.respond(embed=embed)
    elif command == "end":
        embed = discord.Embed(title="Command end")
        embed.add_field(name="_ _", value="Su laimėtojais susisieksime privačia žinute, o apdovanojimai vyks MIDI 2022 Uždarymo vakaro metu.", inline=False)
        embed.set_footer(text="Daugiau informacijos apie Uždarymo vakarą rasite čia: https://fb.me/e/2rmHlGHoW")
        await ctx.respond(embed=embed)
    elif command == "buy":
        embed = discord.Embed(title="Command buy")
        embed.add_field(name="buy <map_index>", value="You can find indices by using default maps command", inline=False)
        embed.set_footer(text="Don't worry you won't lose points if you buy a map you already own")
        await ctx.respond(embed=embed)
    elif command == "hint":
        embed = discord.Embed(title="Command hint")
        embed.add_field(name="hint", value="Sends request for help.**hjelp**", inline=False)
        embed.set_footer(text="IT COSTS COINS")
        await ctx.respond(embed=embed)
    elif command == "leaderboard":
        embed = discord.Embed(title="Command leaderboard/lead/rank")
        embed.add_field(name="leaderboard", value="shows two parties bellow and above you", inline=False)
        await ctx.respond(embed=embed)
    elif command == "style":
        embed = discord.Embed(title="Command style")
        embed.add_field(name="style [red, blue, old]", value="Changes interface", inline=False)
        embed.set_footer(text="It looks \"cool\" yk")
        await ctx.respond(embed=embed)


bot.run(TOKEN)
