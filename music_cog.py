


import discord
from discord.ext import commands
from discord.ext.commands.core import command
from jenkins_cog import JenkinsCog
import youtube_dl

youtube_dl.utils.bug_reports_message = lambda: ''

ffmpeg = "C:/ffmpeg/bin/ffmpeg.exe"

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(self, url, *, loop, stream=False, ytdl):
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return filename, data['title']



class music(JenkinsCog):

    def __init__(self, bot):
        self.bot = bot
        self.ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
        self.voice_channel = None

    async def _check_and_join_channel(self, ctx):
        if ctx.message.author.voice and self.voice_channel == None:
            self.voice_channel = ctx.message.author.voice
            await self.voice_channel.channel.connect()
        else:
            pass


    @commands.command(pass_context = True,
        brief = "Tells me to join your voice channel.",
        description = "Tells me to join your voice channel.")
    async def join(self, ctx):
        if ctx.message.author.voice:
            channel = ctx.message.author.voice.channel
            await channel.connect()
        else:
            await self._send_message(ctx, "You're not in a voice channel")
    


    @commands.command(pass_context = True,
        brief = "Tells me to leave your voice channel.",
        description = "Tells me to join your voice channel.")
    async def leave(self, ctx):
        server = ctx.message.guild.voice_client
        self.voice_channel = None
        # self.queue.clear()
        await server.disconnect()


    @commands.command(pass_context=True,
        brief = "Play's the audio from a youtube url",
        description = "Play's the audio from a youtube url")
    async def play(self, ctx, url):

        await self._check_and_join_channel(ctx)


        try :
            server = ctx.message.guild
            voice_channel = server.voice_client
            
            async with ctx.typing():
                filename, title = await YTDLSource.from_url(url=url, stream=True, loop=self.bot.loop, ytdl=self.ytdl)
                print(filename)
                voice_channel.play(discord.FFmpegPCMAudio(executable=ffmpeg, source=filename))
            await self._send_message(ctx, 'Now playing: {}'.format(title))
        except Exception as e:
            print(str(e))
            await self._send_message(ctx, str(e))

    @play.error
    async def userinfo_error(self, ctx: commands.Context, error: commands.CommandError):
        # if the command above fails for any reason, it will raise `commands.BadArgument`
        # so we handle this in this error handler:

        if isinstance(error, commands.MissingRequiredArgument):
            await self._send_message(ctx, 'I a url to play')


        if isinstance(error, commands.BadArgument):
            await self._send_message(ctx, 'Could not proccess command')

    @commands.command(pass_context=True,
                    brief = "Piano",
                    description = "Piano")
    async def piano(self, ctx):
        await self._check_and_join_channel(ctx)

        server = ctx.message.guild
        voice_channel = server.voice_client
        source = discord.FFmpegPCMAudio(executable=ffmpeg, source="piano.wav")
        voice_channel.play(source)



