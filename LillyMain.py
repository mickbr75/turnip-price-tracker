import datetime
from discord.ext import commands
import random
import RoseSecrets
import copy
import time

bot = commands.Bot(command_prefix='!')
turnips_list = [0,'',0,0,0]
turnips_initial = copy.deepcopy(turnips_list)
turnip_id = 0000


# Shows a list of available commands
@bot.command()
async def commands(ctx):
    await ctx.send("Type !turnips <price> to add your turnips to the price list.")
    await ctx.send("     (without the <> ) ")
    await ctx.send("Type !turnips with no additional parameters to view the top Turnip seller today.")

# Returns a simple Yes or No
@bot.command()
async def yesno(ctx):
    decision = random.choice['yes', 'no']
    await ctx.send("Your answer is " + str(decision))

# Returns a choice from a given list    
@bot.command()
async def choose(ctx, *args):
    decision = random.choice(args)
    await ctx.send("I have chosen " + decision)

# Main Turnips Function
@bot.command()
async def turnips(ctx, arg = 0):
    global turnips_list
    today = datetime.date.today()
    today_day = today.day
    today_month = today.month
    today_hour = time.localtime().tm_hour
    name = str(ctx.message.author)

    if turnips_list[3] < today_day:
        turnips_list[0] = 0
    # AM PM reset, ensures any submission after noon is accepted when compared to a submission made before noon.
    if (turnips_list[4] < 12) & (today_hour >= 12):
        turnips_list[0] = 0
        turnips_list[3] = 0

    if arg == "clear":
        # Sets turnips_list to its initial values
        turnips_list = copy.deepcopy(turnips_initial)
        await ctx.send("Turnip price list cleared.")
        # User Turnip price submission
    elif arg != 0:
        price = int(arg)

        if price >= turnips_list[0]:
            turnips_list[0] = price
            turnips_list[1] = name
            turnips_list[2] = today_month
            turnips_list[3] = today_day
            turnips_list[4] = today_hour
            await ctx.send(name + " submitted their turnips at " + str(int(arg)) + " bells.")
        else:
            await ctx.send("Your turnips at " + str(price) + " bells are less than the current top-seller.")
            await ctx.send("Type !turnips to view theirs.")

    elif arg == 0:
        if turnips_list[3] is today_day:
            #TODO: Format this announcement as a code-block in Discord.
            await ctx.send("Highest current price is: " + str(turnips_list[0]) + " bells. From: " + str(turnips_list[1]))
        else:
            await ctx.send("No turnip prices registered for today. ")

    #TODO: Send a 15-min warning message to the Switch channel at 9:45PM EST that the shop is about to close
    #TODO: Create a help command that explains the Turnip economy and why the bot exists




bot.run(RoseSecrets.Secrets.client_token)
