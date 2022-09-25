from discord.ext import commands

class NabilCog(commands.Cog):
    def __init__(self, bot:commands.Bot, desc:str):
        self.bot = bot
        self.description = desc
        #print(f"{self.__class__.__name__} successfully loaded!")