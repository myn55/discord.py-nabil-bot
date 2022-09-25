import discord
from discord.ext import commands
from .base_cog import NabilCog
from ..utils import *
from random import randint
from colorama import Fore, Style

NO_PROMPT = ["just what are you trying to ask me?", "ask me something first dumbass", "answer WHAT???"]
ANSWERS = ["P yea P", "P i guess P", "P maybe", "P no P", "hell no P"]
DECORATORS = ["lol", "lmao", "lmfao", "bruh", ""]

class FunCog(NabilCog):
    # rng command
    @commands.command(name="rtd", description="Nabil rolls a random number between 1 to 6 or the specified number.", usage="rtd [number|6]")
    async def rtd(self, ctx, number=6):
        num = randint(1, number)
        await ctx.reply(content=f"Rolled number: {num}")
        print(f"Rolled random number: {num}")

    # 8ball command
    @commands.command(name="answer", description="Nabil peers into his vast wisdom and answers your wildest questions.", usage="answer <prompt>")
    async def answer(self, ctx, prompt=None):
        if prompt == None:
            await ctx.reply(NO_PROMPT[randint(0, len(NO_PROMPT))])
            return
        
        answer = ANSWERS[randint(0, len(ANSWERS))]
        i = 0 if bool(randint(0, 1)) else -1
        if answer[i] == "P":
            if i == 0:
                answer = DECORATORS[randint(0, len(DECORATORS))] + answer[1:(-2 if answer[-1] == "P" else len(answer))]
            else:
                answer = answer[(2 if answer[0] == "P" else 0):-1] + DECORATORS[randint(0, len(DECORATORS))]

        await ctx.reply(answer if bool(randint(0, 1)) else answer.upper())
        commandExecuteSuccess("8ball", f"replied to \"{prompt}\" with \"{answer}\"", ctx.author)
        
    # funny DM command
    @commands.command("dm", description="Nabil DMs some poor sod", usage="dm <user ID> <text>")
    async def dm(self, ctx, userID=None, *, text=None):
        # parameter parsing
        if userID == None:
            commandExecuteFailure("DM", "userID not provided", ctx.author)
            await ctx.reply("you didn't give me a user ID")
            return
        else:
            try:
                userID = int(userID)
            except ValueError:
                commandExecuteFailure("DM", "userID isn't a number", ctx.author)
                await ctx.reply("that's not a user ID")
                return

        if text == None:
            commandExecuteFailure("DM", "message text not provided", ctx.author)
            await ctx.reply("you didn't provide anything to send to them")
            return

        # user acquisition
        target:discord.User = None
        try:
            target = await self.bot.fetch_user(userID)
        except discord.NotFound:
            commandExecuteFailure("DM", "userID isn't a number", ctx.author)
            await ctx.reply("couldn't find a person with that ID")
            return
        except discord.HTTPException:
            commandExecuteFailure("DM", "userID isn't a number", ctx.author)
            await ctx.reply("couldn't get the user")
            return

        dm:discord.DMChannel = await target.create_dm()
        try:
            await dm.send(text)
            await ctx.reply(f"message sent to <@{userID}>")
            commandExecuteSuccess("DM", f"sent to {target} \"{text}\"", ctx.author)
        except discord.Forbidden:
            await ctx.reply(f"cannot send messages to this user (<@{userID}>)")
            commandExecuteFailure("DM", f"couldn't send message to user {userID}", ctx.author)

    @commands.command(name="say", aliases=["sm"], description="Nabil says something to a certain channel in a certain server", usage="say")
    async def say(self, ctx):
        guilds = self.bot.guilds
        await ctx.reply(f"which server?\n{', '.join([g.name for g in guilds])}")