"""
#  Main.py
#  On message
if content.startswith("leave"):
    guildname = functions.find_user(str(author.id))
    if guildname:
        functions.leave_guild(str(author.id), guildname)
        role = get(ctx.guild.roles, name=guildname)
        if role:
            await author.remove_roles(role)
        await channel.send("Left the guild successfully")
    else:
        await channel.send("You are not in a guild")
"""

"""
#  Functions.py
def leave_guild(uid, guildname):
    guild = load_guild(guildname)
    guild.members.remove(uid)
    upload_guild(guildname, guild)
    set_guild(uid, None)
    return guildname
"""