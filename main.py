import discord
from discord.ext import commands
from discord.utils import get
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

REGISTER_CHANNEL = 955089619479838802
ADMIN_CHANNEL = 965163235290533928
GUILD_CHANNEL = 959078914083418132


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
        elif channel.id == GUILD_CHANNEL and command == "create":
            if data:
                if not functions.find_user(str(author.id)):
                    if await create_guild(ctx, data):
                        await channel.send(maps.glitch("Guild creation successful"))
                    else:
                        await channel.send(maps.glitch("Guild creation") + " unsuccessful")
                else:
                    await channel.send(maps.glitch("You are already in a party. The organisators prohibited leaving a party"))
            else:
                await channel.send(maps.glitch("You forgot the guild name. ") + "Command is \"create <party_name>\"")
            """await ctx.delete()
            time.sleep(2)
            await answer.delete()"""
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
                    await channel.send(maps.glitch("You are already in a party"))
            else:
                await channel.send(maps.glitch("You forgot the party name.") + "Command is \"join <partyname>\"")
        elif command == "answ":
            result = maps.check_answer(str(author.id), data)
            if result:
                await channel.send(result)
        elif command == "map" or command == "maps":
            if data:
                result = maps.load_map(str(author.id), data)
                if result:
                    await channel.send(embed=result)
                else:
                    await channel.send(maps.glitch("Unidentified map.obj for MX Matrix v1.22474487139"))
            else:
                await channel.send(embed=maps.load_all(str(author.id)))
        elif command == "quest" or command == "quests":
            guild = functions.load_guild(functions.find_user(str(author.id)))
            if data:
                if data.isdigit() and 0 < int(data) < len(guild.questTokens):
                    maps.load_quest(guild.questTokens.keys()[int(data)-1], False)
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
            pass
        elif command == "leaderboard" or command == "lead" or command == "rank":
            if channel.id == ADMIN_CHANNEL:
                result = functions.update_leaderboard()
                if result:
                    await channel.send(maps.glitch(result))
            else:
                guildname = functions.find_user(str(author.id))
                guild = functions.load_guild(guildname)
                await channel.send(embed=guild.lead())
        elif len(ctx.attachments) > 0:
            for file in ctx.attachments:
                sub_channel = get(ctx.guild.channels, id=962275479564468224)
                if file.filename.lower().endswith(".png") or file.filename.lower().endswith(".jpg") or file.filename.lower().endswith(".jpeg"):
                    text = decode.decode_qr(file)
                    text = ' '.join(text.split(" ")[1:])
                    if text:
                        await channel.send(text)
                        """
                        result = maps.get_task(str(author.id), text)
                        if result:
                            await channel.send(result)
                        """
                    else:
                        await sub_channel.send("Unexpected image at channel: <#" + str(channel.id) + ">")
                else:
                    await sub_channel.send("Unexpected attachment at channel: <#" + str(channel.id) + ">")


@bot.slash_command(guild_ids=[928239290440372295], description="No idea")
async def create(ctx):
    await ctx.respond("Guild created", ephemeral=True)


async def create_guild(ctx, guildname):
    try:
        guild = ctx.guild
        member = ctx.author
        guildrole = await guild.create_role(name=guildname.lower(), colour=discord.Colour(0x00FF00))
        await member.add_roles(guildrole)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guildrole: discord.PermissionOverwrite(read_messages=True)
        }
        channel = await guild.create_text_channel(guildname, overwrites=overwrites)
        functions.create_guild(guildname, str(member.id), channel.id)
        # THIS WILL BE VISIBLE:
        await channel.send("Your free map is:")
        await channel.send(embed=maps.load_map(str(member.id), random.choice(["mobil avenue", "zion", "mega city", "backdoor"])))
        await channel.send(embed=maps.load_all(str(member.id)))

        return True
    except Exception as e:
        print(e)
        return False


bot.run(TOKEN)
