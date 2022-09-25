import discord, re
from discord.ext import commands
from .base_cog import NabilCog
from colorama import Fore, Style

class MiscellaneousCog(NabilCog):
    @commands.command(name="help", description="Provides information regarding the bot or certain commands", usage="help [commandName]")
    async def help(self, ctx, commandName=None):
        helpEmbed = discord.Embed()

    @commands.command(name="ping", description="Pings the bot (user) and returns latency in ms", usage="ping")
    async def ping(self, ctx):
        latency = int(self.bot.latency*1000)
        await ctx.send(f"{latency}ms, {'fine' if self.bot.latency < 150 else 'alarming'}")
        print(f"Checked ping ({latency}ms) [{ctx.author}]")

    @commands.command(name="shutdown", description="Shuts down Nabil (only current universe Nabil can)", usage="shutdown")
    async def shutdown(self, ctx):
        if ctx.author.id == self.bot.owner_id:
            await ctx.reply("N")
            print(Fore.RED+"\nShutting down..."+Style.RESET_ALL)
            await self.bot.close()

    @commands.command(name="userinfo", description="Displays information about a user", usage="userinfo [user]")
    async def userinfo(self, ctx, user=None):
        target = None
        if user == None:
            target = ctx.author
        else:
            match = re.match("^<@(\d+)>$", user)
            if match:
                # ping
                target = await self.bot.fetch_user(int(match.group(1)))
            else:
                await ctx.reply("couldn't find that person")
                return

        infoEmbed = discord.Embed(title=f"Information about {target}", color=target.color)
        infoEmbed.set_thumbnail(url=target.avatar_url)
        infoEmbed.set_author(name=f"ID {target.id}")
        await ctx.send(embed=infoEmbed)
