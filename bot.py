import discord
from discord import Game
from discord.ext import commands
import os
from dotenv import load_dotenv

import dice_roll

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
async def on_commmand(context):

    print(context)

@bot.event
async def on_message(message):
    print(message)
    await bot.process_commands(message) 

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you"))



@bot.command()
async def test(ctx: commands.Context, arg):
    await _send_message(ctx, arg)

@bot.command()
async def roll(ctx, *, arg):
    try:
       response =  dice_roll.roll(arg)

    except Exception:
        await _send_message(ctx, 'Format must include a string of rolls to make')
        return

    await _send_message(ctx, response)


@roll.error
async def userinfo_error(ctx: commands.Context, error: commands.CommandError):
    # if the command above fails for any reason, it will raise `commands.BadArgument`
    # so we handle this in this error handler:
    if isinstance(error, commands.BadArgument):
        return await _send_message(ctx, 'Could not proccess command')

bot.run(TOKEN)

