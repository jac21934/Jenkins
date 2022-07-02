import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# import dice_roll
# import player
from music_cog import music
from game_cog import game

load_dotenv()
TOKEN = os.getenv('TOKEN')
GUILD_ID = os.getenv('GUILD_ID')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), intents=intents, description="A GMing bot.")

def _build_message(msg:str) -> str:
    message = '```' + msg + '```'
    return message

async def _send_message(ctx, msg:str):
    await ctx.send(_build_message(msg))


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you"))

# @bot.event
# async def on_message(message):
#     print(message)
#     ctx = await bot.get_context(message)
#     async with ctx.typing():
#         await bot.process_commands(message) 

# Close
@bot.command(brief="Shuts me down.",
    description="Shuts me down.")
async def close(ctx):
    await _send_message(ctx, 'Shutting down.')
    await bot.close()

# Delete command
@bot.command(brief="Delete's this command's message", 
    description="Delete's the message that invokes this command. This has no point.")
async def delete(ctx):
    await ctx.message.delete()

# Say
@bot.command(hidden=True)
async def say(ctx, *, arg):
    await ctx.message.delete()
    await _send_message(ctx, arg)

#ping w/ message
@bot.command(hidden=True)
async def ping_message(ctx, role:discord.Role, *, msg):
    await ctx.message.delete()
    await ctx.send(f"{role.mention}")
    await _send_message(ctx, msg)

bot.add_cog(music(bot))
bot.add_cog(game(bot))


bot.run(TOKEN)

