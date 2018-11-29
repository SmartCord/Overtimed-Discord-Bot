import traceback, discord
import datetime, random
from tools.bot_tools import db

default_prefix = "?"
c = 0x0a91ff
g = 0x18d45c
r = 0xff4343

gif = {
    'no1':'https://media.giphy.com/media/6Q2KA5ly49368/giphy.gif',
    'disappointed1':'https://media.giphy.com/media/U4VXRfcY3zxTi/giphy.gif'
}

def color():
    return random.choice([0xff66c1, 0x6666c1, 0xb0d996, 0x588585, 0x21ff94, 0x1d4457, 0x77003c, 0x936dd4, 0xd46db6, 0x48cfa6])

def prefix(message):
    try:
        if db.server_prefixes.count({"server_id":message.guild.id}):
            return [x['prefix'] for x in db.server_prefixes.find({"server_id":message.guild.id})][0]
        return default_prefix
    except:
        return default_prefix

def icon(ctx, guild):
    try:
        return guild.icon_url if guild.icon_url != "" else ctx.me.avatar_url
    except:
        try:
            return ctx.me.avatar_url
        except:
            try:
                return ctx.author.avatar_url
            except:
                return None

async def usage(ctx, arguments, example, description):
    prefix = prefix(ctx)
    args = [f"<{arg}>" for arg in arguments]
    arguments = " ".join(args)
    example = " ".join(example)
    command = ctx.command.qualified_name
    e = discord.Embed(title="Wrong Usage", color=color())
    e.add_field(name="Proper Usage", value=f"{prefix}{command} {arguments}")
    e.add_field(name="\u200b", value="\u200b")
    e.add_field(name="Example", value=f"{prefix}{command} {example}")
    e.add_field(name="Description", value=description)
    e.set_thumbnail(url=gif['no1'])
    footer(ctx, e)
    await ctx.send(embed=e)

async def error(ctx, error, description):
    e = discord.Embed(title=error, description=description, color=r)
    e.set_thumbnail(url=ctx.me.avatar_url)
    footer(ctx, e)
    await ctx.send(embed=e)

async def success(ctx, message, image=None):
    e = discord.Embed(title="Success!", description=message, color=g)
    try:
        e.set_thumbnail(url=ctx.avatar_url) if not image else None
    except:
        e.set_thumbnail(url=ctx.author.avatar_url) if not image else None
    e.set_image(url=image) if image else None
    footer(ctx, e)
    await ctx.send(embed=e)

def footer(ctx, embed, extra=None):
    try:
        if ctx.author.avatar_url:
            avatar = ctx.author.avatar_url
        else:
            avatar = ctx.me.avatar_url
        author = ctx.author
    except:
        avatar = ctx.avatar_url
        author = ctx
    embed.timestamp = datetime.datetime.utcnow()
    if extra is None:
        extra = ""
    else:
        extra = " " + extra
    embed.set_footer(text=f"{author}{extra}", icon_url=avatar)

async def botError(bot, message, e):
    e = traceback.format_exc()
    em = discord.Embed(title="Oh well an unexpected error has occured", description=f"```{e}```\nThe error has now been sent to the bot developer. (Thank goodness)", color=r)
    em.set_thumbnail(url=gif['disappointed1'])
    footer(message, em)
    await message.send(embed=em)

    if message.author.id == 363880571614527488: # Your ID
        return

    ctx = bot.get_channel(517276933344460820) # Channel to send message
    em = discord.Embed(title=f"Command Error", description=f"Command : {message.message.content}\n \
    User : {message.author} ({message.author.id})\n \
    Server : {message.guild} ({message.guild.id})", color=r)
    em.add_field(name="Error", value=f"```{e}```")
    if message.author.avatar_url:
        a = message.author.avatar_url
    else:
        a = message.me.avatar_url
    em.set_thumbnail(url=a)
    await ctx.send(embed=em)
