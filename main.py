from imports import *

async def run():
    bot = LeEpic()
    await bot.start(config.bot_token)

class LeEpic(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=self._get_shagger_prefix)
        self.loop.create_task(self.load_modules())
        self.loads_xd = []

    async def _get_shagger_prefix(self, bot, message):
        return "!."

    async def load_modules(self):
        await self.wait_until_ready()
        modules = [x.stem for x in Path('modules').glob('*.py')]
        for module in modules:
            try:
                self.load_extension(f'modules.{module}')
                print(f"Loaded {module}")
                self.loads_xd.append(f"Loaded {module}")
            except Exception as e:
                print(f"Failed to load {module} : {e}")
                self.loads_xd.append(f"Failed to load {module} : {e}")

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            return await utils.error(ctx, "Bad Argument", str(error))


    async def on_ready(self):
        channel = self.get_channel(517272487201865728)
        oof = "\n".join(self.loads_xd)
        e = discord.Embed(title="The bot have launched", description=f"```{oof}```", color=color())
        e.set_thumbnail(url=self.user.avatar_url)
        footer(self.user, e)
        await channel.send(embed=e)
        print("Ok this is epic")

    async def on_message(self, message):
        Counters.messages_sent += 1
        if message.author.bot:
            return

        if message.content == "?server_prefix":
            await message.channel.send(f"The prefix for this server is : {prefix(message)}")

        await self.process_commands(message)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
