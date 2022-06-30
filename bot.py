import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

import dice_roll
import player
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


# Roll
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

# Close
@bot.command(description="Shuts me down.")
async def close(ctx):
    await _send_message(ctx, 'Shutting down.')
    await bot.close()
# Players
@bot.command()
async def players(ctx):
    message = player.list_players()
    await _send_message(ctx, message)

# Stats
@bot.command(brief="Prints the stats of a player.", 
    description = "Prints the stats of a player. If a name is given, prints the stats of that player, otherwise prints the stats of the player that envokes the command",
    category="Game Commands")
async def stats(ctx, *, arg=None):
    print(ctx)
    p = None
    msg = ""

    if arg == None:
        print("HERE")
        print(ctx.author.id)
        p = player.get_player_from_id(str(ctx.author.id))
    else:
        p = player.get_player_from_name(arg)

    if p == None:
        msg = "Unrecognized player"

    else:
        msg = player.print_player(p)

    await _send_message(ctx, msg)


@bot.command(brief="Delete's this command message", description="Delete's the message that invokes this command. This has no point.")
async def delete(ctx):
    await ctx.message.delete()


@bot.command(hidden=True)
async def say(ctx, *, arg):
    await ctx.message.delete()
    await _send_message(ctx, arg)

@bot.command(hidden=True)
async def ping_message(ctx, role:discord.Role, *, msg):
    await ctx.message.delete()
    await ctx.send(f"{role.mention}")
    await _send_message(ctx, msg)


@bot.command(hidden=True)
async def test(ctx, arg1, *, arg):
    await ctx.message.delete()
    await _send_message(ctx, arg1)
    await _send_message(ctx, arg)

bot.run(TOKEN)

