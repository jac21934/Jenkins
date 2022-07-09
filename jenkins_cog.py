import discord
from discord.ext import commands
from discord.ext.commands.core import command

class JenkinsCog(commands.Cog):
    def _init(self):
        pass
    
    def _build_message(self, msg:str) -> str:
        message = '```' + msg + '```'
        return message

    async def _send_message(self, ctx, msg:str):
        await ctx.send(self._build_message(msg))
