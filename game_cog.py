from discord.ext import commands
from discord.ext.commands.core import command
from jenkins_cog import JenkinsCog
import player
import dice_roll



class game(JenkinsCog):


    #roll command
    @commands.command(pass_context = True,
        brief = "Rolls dice for players.",
        description = "Rolls dice based on XdY +/- Z format. Advantage and disadvantage can be used as well by including adv or dis in the command.")
    async def roll(self, ctx, *, arg):
        msg = arg.casefold() 
        p = None
        try:
            p = player.get_player_from_id(str(ctx.author.id))
            response =  dice_roll.roll(msg, p)

        except Exception as e:
            print(str(e))

            await self._send_message(ctx, str(e))
            return

        await self._send_message(ctx, response)


    @roll.error
    async def userinfo_error(self, ctx: commands.Context, error: commands.CommandError):
        # if the command above fails for any reason, it will raise `commands.BadArgument`
        # so we handle this in this error handler:

        if isinstance(error, commands.MissingRequiredArgument):
            await self._send_message(ctx, 'I need dice values to roll')


        if isinstance(error, commands.BadArgument):
            await self._send_message(ctx, 'Could not proccess command')

    # Players
    @commands.command(pass_context = True,
        brief = "Lists players and levels.",
        description="Lists players and levels.")
    async def players(self, ctx):
        message = player.list_players()
        await self._send_message(ctx, message)

    # Stats
    @commands.command(pass_context = True, 
        brief="Prints the stats of a player.", 
        description = "Prints the stats of a player. If a name is given, prints the stats of that player, otherwise prints the stats of the player that envokes the command")
    async def stats(self, ctx, *, arg=None):
        print(ctx)
        p = None
        msg = ""

        if arg == None:
            p = player.get_player_from_id(str(ctx.author.id))
        else:
            p = player.get_player_from_name(arg)

        if p == None:
            msg = "Unrecognized player"

        else:
            msg = player.print_player(p)

        await self._send_message(ctx, msg)