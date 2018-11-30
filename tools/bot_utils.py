from imports import *

class AchievementNotFound(Exception):
    pass

class UserNotFound(Exception):
    pass

async def giveAchievement(user, id):
    if not db.achievements.count({"id":id}):
        raise AchievementNotFound('Srry mate but that achievement is not found. hehehe gaddem')

    if not db.profiles.count({"user_id":user.id}):
        raise UserNotFound('How sad :(')

    achievements = [x['achievements'] for x in db.profiles.find({"user_id":user.id})][0]
    if not id in achievements:
        db.profiles.update_one({"user_id":user.id}, {'$push':{'achievements':id}})

    for x in db.achievements.find({"id":id}):
        reward = f"<:gold:514791023671509003> {x['coins']} Coins\n<:diagay:515536803407593486> {x['diamonds']} Diamonds"
        e = discord.Embed(title=f"Wow New Achievement! Such cool", description=f":clap: Congratulations {user.name} you just obtained the achievement {x['name']}. :clap:\n\nOh and here are your rewards\n{reward}", color=color())
        e.set_thumbnail(url=gif['clap1'])
        footer(user, e)
        await user.send(embed=e)
        db.profiles.update_one({"user_id":user.id}, {'$inc':{'coins':x['coins'], 'diamonds':x['diamonds']}})