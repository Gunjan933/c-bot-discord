import os, random, discord
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
OWNERID = os.getenv('OWNERID')

bot = commands.Bot(command_prefix='-')

@bot.event
async def on_command_error(ctx, error):
  await ctx.send(f'Try `-help` \n[{error}]')

@bot.command()
async def hey(ctx):
  hey_quotes = [
    'I\'m the human form of the 💯 emoji.',
    'Bingpot!',
    (
      'Cool. Cool cool cool cool cool cool cool, '
      'no doubt no doubt no doubt no doubt.'
    ),
  ]

  response = random.choice(hey_quotes)
  await ctx.send(response)

@bot.command(name='ping', help='checks latency.')
async def ping(ctx):
  await ctx.send(f'~{round (bot.latency * 1000)}ms')


@bot.command()
async def shutdown(ctx):
  if int(ctx.message.author.id) == int(OWNERID):
    try:
      await bot.logout()
      print("shutting down")
    except:
      bot.clear()
      print("Environment Error")
  else:
    await ctx.send("You do not own this bot!")


bot.remove_command('help')

@bot.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(colour = discord.Colour.green())
    embed.add_field(name='Cainvas Bot', value='Made with :heart: by **AITS**', inline=False)
    embed.add_field(name='-help', value='list of commands available', inline=False)
    embed.add_field(name='-ping', value='checks latency.', inline=False)
    embed.add_field(name='-hey', value='generates random quote.', inline=False)
    embed.add_field(name='-shutdown', value='shuts down cainvas bot', inline=False)
    await ctx.send(embed=embed)



bot.run(TOKEN)