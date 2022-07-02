


import discord
from discord import FFmpegPCMAudio, PCMVolumeTransformer
from discord.ext import commands, tasks
from discord.ext.commands.core import command
from jenkins_cog import JenkinsCog

import os
from googleapiclient.discovery import build
from dotenv import load_dotenv



class music(JenkinsCog):

    def __init__(self, bot):
        load_dotenv()
        self.API_KEY = os.environ.get('GOOGLE_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.API_KEY)

        self.bot = bot
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}

    @commands.command(pass_context = True)
    async def join(self, ctx):
        if ctx.message.author.voice:
            channel = ctx.message.author.voice.channel
            await channel.connect()
        else:
            await self._send_message(ctx, "You're not in a voice channel")
    
    @commands.command(pass_context = True)
    async def leave(self, ctx):
        server = ctx.message.guild.voice_client
        # self.queue.clear()
        await server.disconnect()

