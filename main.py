import discord, json
from discord.ext import commands
from resources.cogs.fun import FunCog
from resources.cogs.management import ManagementCog
from resources.cogs.miscellaneous import MiscellaneousCog
from colorama import init, Fore, Back, Style
from art import text2art
from datetime import datetime
init()

NABIL_ID = 313448715035869185

class NabilBot(commands.Bot):
    messageBlackList = []

    async def on_ready(self):
        self.owner_id = NABIL_ID
        print(Fore.YELLOW+text2art("Nabil [AU]")+Fore.GREEN+f"Successfully logged on as {Fore.CYAN+Style.BRIGHT+str(client.user)}\n{Fore.WHITE+str(datetime.now())}")
        print(Style.RESET_ALL)

    async def on_message(self, message:discord.Message):
        if message.content.lower().startswith("nabil "):
            await self.process_commands(message)
        else:
            if message.author.id in self.messageBlackList:
                pass

    async def on_command_error(self, context, exception):
        if type(exception) == commands.errors.CommandNotFound:
            print(Fore.RED+f"{exception}"+Style.RESET_ALL)
        else:
            await context.reply(f"something wrong happened (better ping nabil)\n```{exception}\n```")

client = NabilBot("nabil ", help_command=None)
settings = open("settings.json")

client.add_cog(FunCog(client, "Funny commands"))
client.add_cog(ManagementCog(client, "Server-related commands"))
client.add_cog(MiscellaneousCog(client, "Niche commands"))
client.run(json.load(settings)["token"])
settings.close()
