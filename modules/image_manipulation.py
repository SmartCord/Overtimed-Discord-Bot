from imports import *

def wrap(font, text, line_width):
    words = text.split()
    lines = []
    line = []
    for word in words:
        newline = ' '.join(line + [word])
        w,h = font.getsize(newline)
        if w > line_width:
            lines.append(' '.join(line))
            line = [word]
        else:
            line.append(word)
    if line:
        lines.append(' '.join(line))
    return '\n'.join(lines)

def add_corners(im, rad=10):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, "white")
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im

def ReduceOpacity(img, opacity):
    assert opacity >= 0 and opacity <= 1
    img = img.copy()
    x = img.split()[3]
    x = ImageEnhance.Brightness(x)
    x = x.enhance(opacity)
    img.putalpha(x)
    return img

def change_contrast(img, level):
    factor = (259 * (level + 255)) / (255 * (259 - level))
    def contrast(c):
        return 128 + factor * (c - 128)
    return img.point(contrast)

class ImageManipulation:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def spiderglasses(self, ctx, user1: discord.Member = None, user2: discord.Member = None):
        try:
            if user2 is None:
                user2 = ctx.author
            if user1 is None:
                return await usage(ctx, ['mention a user', 'mention the second user'], [ctx.author.mention, ctx.me.mention], 'Puts the two user\'s avatar in a spiderman glasses meme.')

            size = (210, 210)
            base = Image.open("assets/spiderglasses.jpg")

            u1 = requests.get(user1.avatar_url)
            u2 = requests.get(user2.avatar_url)

            url1 = BytesIO(u1.content)
            url1 = Image.open(url1).resize(size).convert('RGBA')
            url1 = url1.filter(ImageFilter.BLUR)
            url1 = url1.filter(ImageFilter.BLUR)
            url1 = url1.filter(ImageFilter.BLUR)
            url1 = url1.filter(ImageFilter.BLUR)
            url1 = url1.filter(ImageFilter.BLUR)
            url1 = url1.filter(ImageFilter.BLUR)
            url1 = url1.filter(ImageFilter.BLUR)
            url1 = url1.filter(ImageFilter.BLUR)

            url2 = BytesIO(u2.content)
            url2 = Image.open(url2).resize(size).convert('RGBA')

            base.paste(url1, (279,18), url1)
            base.paste(url2, (279,283), url2)
            file = BytesIO()
            base.save(file, "png")
            file.seek(0)

        except Exception as e:
            await botError(self.bot, ctx, e)

def setup(bot):
    bot.add_cog(ImageManipulation(bot))
