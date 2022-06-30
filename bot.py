import discord
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
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you"))



@bot.command()
async def roll(ctx, *, arg):
    msg = arg.casefold() 
    try:
        response =  dice_roll.roll(msg)

    except Exception as e:
        print(str(e))

        await _send_message(ctx, str(e))
        return

    await _send_message(ctx, response)


@roll.error
async def userinfo_error(ctx: commands.Context, error: commands.CommandError):
    # if the command above fails for any reason, it will raise `commands.BadArgument`
    # so we handle this in this error handler:

    if isinstance(error, commands.MissingRequiredArgument):
        await _send_message(ctx, 'I need dice values to roll')


    if isinstance(error, commands.BadArgument):
        await _send_message(ctx, 'Could not proccess command')


@bot.command()
async def close(ctx):
    await _send_message(ctx, 'Shutting down.')
    await bot.close()


bot.run(TOKEN)

