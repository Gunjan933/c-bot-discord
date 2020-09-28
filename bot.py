import os, random, discord, asyncio
from discord.ext import commands
from dotenv import load_dotenv

from utils.database import bot_database
database = bot_database()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
OWNERID = os.getenv('OWNERID')
SYNC_AFTER = 15*60   #15 minutes


bot = commands.Bot(command_prefix='-')

def owner(ctx):
  return int(ctx.message.author.id) == int(OWNERID)

def admin(ctx):
  return ctx.message.author.guild_permissions.administrator

def current_user(ctx):
  return str(ctx.message.author)

async def auto_sync():
  await bot.wait_until_ready()
  while not bot.is_closed():
    if database.sync_with_spreadsheet():
      print("Database synced")
    else:
      print("Database not synced")
    await asyncio.sleep(SYNC_AFTER)

@bot.event
async def on_command_error(ctx, error):
  await ctx.send(f'Try `-help` \n[{error}]')

@bot.command()
async def search(ctx, uniqueID=None):
  if not uniqueID:
    uniqueID = current_user(ctx)
  if admin(ctx):
    await ctx.send(database.search(uniqueID, admin=True))
  else:
    await ctx.send(database.search(uniqueID, admin=False))


@bot.command()
async def sync(ctx):
  if admin(ctx):
    if database.sync_with_spreadsheet():
      response = "Database synced"
    else:
      response = "Database not synced"
  else:
    response = "You are not an admin!"
  await ctx.send(response)


@bot.command()
async def ping(ctx):
  await ctx.send(f'{round (bot.latency * 1000)}ms')


@bot.command()
async def shutdown(ctx):
  if owner(ctx):
    try:
      await ctx.send("Shutting down!")
      await bot.logout()
    except:
      await ctx.send("Environment Error")
      bot.clear()
  else:
    await ctx.send("You do not own this bot!")



@bot.event
async def on_member_join(member):
  channel = discord.utils.get(member.guild.text_channels, name="new-joiners")
  await channel.send(f"{member} has arrived!")


bot.remove_command('help')
@bot.command(pass_context=True)
async def help(ctx):
  embed = discord.Embed(colour = discord.Colour.green())
  embed.add_field(name='Cainvas Bot', value='Made with :heart: by **AITS**', inline=False)
  embed.add_field(name='-help', value='list of commands available', inline=False)
  embed.add_field(name='-search [discord ID | cainvas ID | email address]', value='searches for user', inline=False)
  embed.add_field(name='-ping', value='checks latency.', inline=False)
  embed.add_field(name='-sync', value='syncs database *(requires admin privilage)*', inline=False)
  embed.add_field(name='-shutdown', value='shuts down cainvas bot *(requires ownership privilage)*', inline=False)
  await ctx.send(embed=embed)



bot.loop.create_task(auto_sync())
bot.run(TOKEN)