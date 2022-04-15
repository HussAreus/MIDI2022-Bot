import discord
from discord.ext import commands
from discord.utils import get
import functions
import maps
import decode
import time
import random
import os
"""
Requires (pip install <module>):
discord
discord.ext
opencv-python
pyzbar
"""

REGISTER_CHANNEL = 955089619479838802
japanese = "あいうえおかきくけこがげぎぐごさしすせそざじずぜぞたちつてとだぢづでどなにぬねのはひふへほばびぶべぼぱぴぷぺぽまみむめもやゆよらりるれろわをん"
bot = commands.Bot(command_prefix="")
TOKEN = os.environ["TOKEN"]


@bot.event
async def on_ready():
    print("Satoshi Nakamoto ready to serve")


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
        elif command == "green":
            await channel.send("```bash\n\"Green Text hopefully\"\n```")
        elif command == "create":
            if data:
                if not functions.find_user(str(author.id)):
                    if await create_guild(ctx, data):
                        await channel.send("Guild creation successful")
                    else:
                        await channel.send("Guild creation unsucessful")
                else:
                    await channel.send("You are already in a guild. Use leave command to leave")
            else:
                await channel.send("You forgot the guild name. Command is \"create <guildname>\"")
            """await ctx.delete()
            time.sleep(2)
            await answer.delete()"""
        elif command == "join":
            if data:
                if not functions.find_user(str(author.id)):
                    result, memb = functions.join(str(author.id), data)
                    if result and memb:
                        role = get(ctx.guild.roles, name=data.lower())
                        if role:
                            await author.add_roles(role)
                        await channel.send("Joined the guild successfully")
                    elif result:
                        await channel.send("Guild is full")
                else:
                    await channel.send("You are already in a guild. Leave current guild before ")
            else:
                await channel.send("You forgot the guild name. Command is \"join <guildname>\"")
        elif command == "answ":
            result = maps.check_answer(str(author.id), data)
            if result:
                await channel.send(result)
        elif command == "map" or command == "maps":
            data = content.split(" ")
            data = data[1:]
            data = ' '.join(data)
            if data:
                result = maps.load_map(str(author.id), data)
                if result:
                    await channel.send(embed=result)
                else:
                    await channel.send("BRUH NO?")
            else:
                await channel.send(embed=maps.load_all(str(author.id)))
        elif command == "style":
            data = content.split(" ")
            data = data[1:]
            data = ' '.join(data)
            guildname = functions.find_user(str(author.id))
            guild = functions.load_guild(guildname)
            if data and guild:
                result = guild.set_style(data)
                if result:
                    functions.upload_guild(guild)
                    await channel.send("Interface style changed to \""+data+"\"")
                else:
                    await channel.send("No such style in databases")
        elif command == "buy":
            data = content.split(" ")
            data = data[1:]
            data = ' '.join(data)
            embed = maps.buy_map(str(author.id), data)
            if embed:
                await channel.send(embed=embed)
        elif command == "hint":
            pass
        elif len(ctx.attachments) > 0:
            for file in ctx.attachments:
                sub_channel = get(ctx.guild.channels, id=962275479564468224)
                if file.filename.lower().endswith(".png") or file.filename.lower().endswith(".jpg") or file.filename.lower().endswith(".jpeg"):
                    text = decode.decode_qr(file)
                    if text:
                        await channel.send(text)
                        """
                        result = maps.get_task(text)
                        if result:
                            await channel.send(result)"""
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



rand ="OTUzNzQ2NjM0NzU4NTc0MTMw.YjJDxQ.NaJXilXrIQR5oQ3lq0ac_hFVjXg"
bot.run(TOKEN)
