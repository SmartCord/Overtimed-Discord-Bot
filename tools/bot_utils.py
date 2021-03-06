from imports import *

class Counters:
    profiles_since_restart = 0
    messages_sent = 0

class AchievementNotFound(Exception):
    pass

class UserNotFound(Exception):
    pass

class CommandNotFound(Exception):
    pass

def getPoints(command):
    if db.commands.count_documents({"name":command}):
        return [x['points'] for x in db.commands.find({"name":command})][0]
    else:
        raise CommandNotFound("The command {} is not found.".format(command))

async def pointlessRaw(ctx):
    req_points = 0
    if db.commands.count({"name":ctx.command.qualified_name}):
        req_points = [x['points'] for x in db.commands.find({"name":ctx.command.qualified_name})][0]
    user_points = [x['points'] for x in db.profiles.find({"user_id":ctx.author.id})][0]
    left = user_points - req_points
    if left < 0:
        return True
    return False


async def pointless(ctx):
    req_points = 0
    if db.commands.count({"name":ctx.command.qualified_name}):
        req_points = [x['points'] for x in db.commands.find({"name":ctx.command.qualified_name})][0]
    user_points = [x['points'] for x in db.profiles.find({"user_id":ctx.author.id})][0]
    left = user_points - req_points
    s = "s"
    if req_points < 2:
        s = ""
    if user_points == 0:
        but = "but you no longer have any points."
    elif user_points == 1:
        but = "but you only have 1 point left."
    else:
        but = "but you only have {} points left.".format(user_points)
    if left < 0:
        e = discord.Embed(title="Not enough points", description=f"Sorry but this command requires {req_points} point{s} {but} Please visit the store to buy more points.", color=color())
        e.set_thumbnail(url=ctx.author.avatar_url)
        footer(ctx, e)
        return await ctx.send(embed=e), True
    return False

async def giveAchievement(user, id, extra=None):
    if extra is None:
        extra = ""

    if not db.achievements.count({"id":id}):
        raise AchievementNotFound('Sorry mate but that achievement is not found. hehehe gaddem')

    if not db.profiles.count({"user_id":user.id}):
        raise UserNotFound('How sad :(')

    achievements = [x['achievements'] for x in db.profiles.find({"user_id":user.id})][0]

    if id in achievements:
        return

    #if not id in achievements:
    db.profiles.update_one({"user_id":user.id}, {'$push':{'achievements':id}})

    for x in db.achievements.find({"id":id}):
        reward = f"<:gold:514791023671509003> {x['coins']} Coins\n<:diagay:515536803407593486> {x['diamonds']} Diamonds"
        e = discord.Embed(title=f"Wow New Achievement! Such cool", description=f":clap: Congratulations {user.name} you just obtained the achievement {x['name']} {extra}. :clap:\n\nOh and here are your rewards\n{reward}", color=color())
        e.set_thumbnail(url=utils.gif['clap1'])
        footer(user, e)
        await user.send(embed=e)
        db.profiles.update_one({"user_id":user.id}, {'$inc':{'coins':x['coins'], 'diamonds':x['diamonds']}})
