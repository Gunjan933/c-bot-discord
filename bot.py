import os, random, discord
from discord.ext import commands
from dotenv import load_dotenv

from utils.database import bot_database
database = bot_database()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
OWNERID = os.getenv('OWNERID')

bot = commands.Bot(command_prefix='-')

def owner(ctx):
  return int(ctx.message.author.id) == int(OWNERID)

def admin(ctx):
  return ctx.message.author.guild_permissions.administrator

def current_user(ctx):
  return "{}#{}".format(ctx.message.author.name, ctx.message.author.id)

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


@bot.command()
async def search(ctx, uniqueID=None):
  if not uniqueID:
    uniqueID = current_user(ctx)
  df = database.search(uniqueID)
  if not df.empty:
    if admin(ctx):
      response = df.to_string(index = False)
    else:
      columns = ['First Name', 'Last Name', 'cAInvas User Name', 'Email Address']
      response = (df[columns]).to_string(index = False)
  else:
    response = "No users found with {}".format(uniqueID)
  await ctx.send(response)


@bot.command()
async def sync(ctx):
  if owner(ctx):
    database.sync_with_spreadsheet()
    await ctx.send(f'synced database')
  else:
    await ctx.send("You do not own this bot!")


@bot.command()
async def ping(ctx):
  await ctx.send(f'~{round (bot.latency * 1000)}ms')


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

# channel = discord.utils.get(guild.text_channels, name="new-joiners")
# print(channel.id)
# @commands.Cog.listener()
# async def on_member_join(self, member):
#     ment = member.mention
#     await self.client.get_channel(channel id).send(f"{ment} has joined the server.")
#     print(f"{member} has joined the server.")


bot.remove_command('help')

@bot.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(colour = discord.Colour.green())
    embed.add_field(name='Cainvas Bot', value='Made with :heart: by **AITS**', inline=False)
    embed.add_field(name='-help', value='list of commands available', inline=False)
    embed.add_field(name='-ping', value='checks latency.', inline=False)
    embed.add_field(name='-search', value='searches for user.', inline=False)
    embed.add_field(name='-hey', value='generates random quote.', inline=False)
    embed.add_field(name='-shutdown', value='shuts down cainvas bot', inline=False)
    await ctx.send(embed=embed)



bot.run(TOKEN)