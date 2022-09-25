import discord
import os
from discord.ext import commands
from .base_cog import NabilCog
from ..utils import *
from colorama import Fore, Style
from asyncio import TimeoutError
from datetime import datetime

def logPurge(deleted, ctx:commands.Context):
    deleted.reverse()
    log = open(f"logs/purges/{ctx.author} in {ctx.guild.name} [{len(deleted)}, {ctx.message.id}].txt", "w")

    entries = []
    entry = ""
    for msg in deleted:
        entry = f"[{msg.created_at} UTC] {msg.author}: {msg.clean_content}"
        entries.append(entry)

    log.writelines([e+"\n" for e in entries])
    log.close()

class ManagementCog(NabilCog):
    @commands.command(name="purge", description="Purges a number of messages in the respective channnel", usage="purge <number>")
    async def purge(self, ctx, number=None):
        author = ctx.message.author
        # TODO check perms

        channel:discord.TextChannel = ctx.channel

        if number == None:
            commandExecuteFailure("purge", "message number not delivered", author)
            await ctx.reply("you didn't give me a number of messages to purge")
            return
        else:
            try:
                number = int(number)
            except ValueError:
                commandExecuteFailure("purge", "valid number not delivered", author)
                await ctx.reply("I don't think that's a number")
                return

        if number >= 20:
            confirmation:discord.Message = await ctx.send("are you sure? (y/n)")
            try:
                while True:
                    msg:discord.Message = await self.bot.wait_for("message", check=lambda m:(m.author == author), timeout=10)
                    content = msg.content.lower()
                    if content == "y" or content == "yes":
                        await msg.delete()
                        await confirmation.delete()
                        break
                    elif content == "n" or content == "no":
                        commandExecuteFailure("purge", "confirmation timeout", author)
                        await ctx.send("halting purge")
                        return
            except TimeoutError:
                await ctx.send(content="timeout reached")

        await ctx.message.delete()
        deleted = await channel.purge(limit=number)
        logPurge(deleted, ctx)
        commandExecuteSuccess("purge", f"#{channel}, {len(deleted)} messages", ctx.message.author)
        await ctx.send(content=f"deleted {len(deleted)} messages", delete_after=3)