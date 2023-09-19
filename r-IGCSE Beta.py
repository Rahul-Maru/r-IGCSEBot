import os
import nextcord as discord
from nextcord.ext import tasks, commands
import calendar
import time
from pytz import timezone

TOKEN = "OTQ3ODU3NDY3NzI2MDAwMTU4.G0Zej1.IbamQIeHL7159ldgrdMXAmwvLtjyboQ9YpgBVE"
GUILD_ID = 1111128710133854289

intents = discord.Intents().all()
bot = commands.Bot(command_prefix=".", intents=intents)

async def isModerator(member: discord.Member):
    roles = [role.id for role in member.roles]
    if 1122762930216255612 in roles or 1151522478288552046 in roles:  # r/igcse moderator role ids
        return True
    elif member.guild_permissions.administrator:
        return True
    return False

async def hasRole(member: discord.Member, role_name: str):
    roles = [role.name.lower() for role in member.roles]
    for role in roles:
        if role_name.lower() in role:
            return True
    return False

@bot.event 
async def on_ready():
	print(f"Logged in as {str(bot.user)}.")
	await bot.change_presence(activity=discord.Game(name="Flynn#5627"))

@bot.event
async def on_message(message:discord.Message):
    message_channel = message.channel.id
    message_author = message.author.id
    message_content = message.content
    if message_channel == 1153283974211321906:
        if message.author.bot: print(message_content)
        else: await message.delete()
    else: return
    

@bot.slash_command(name="channellock", description="locks a channel at a specified time")
async def lockcommand(interaction: discord.Interaction,
                        channel: discord.TextChannel =  discord.SlashOption(name="channel_name", description="Which channel do you want to lock?", required=True),
                        locktime: str = discord.SlashOption(name="lock_time", description="At what time do you want the channel to be locked?", required=True),
                        unlocktime: str = discord.SlashOption(name="unlock_time", description="At what time do you want the channel to be unlocked?", required=True)):
       locktimeinunix = f"<t:{locktime}:F>"
       unlocktimeinunix = f"<t:{unlocktime}:F>"       
       await interaction.send(f"<#{channel.id}> is scheduled to lock at {locktimeinunix} and unlock at {unlocktimeinunix}", ephemeral=True)
       channelid = f"<#{channel.id}>"
       channel = bot.get_channel(1153283974211321906)
       await channel.send(f'Channel Name: {channelid}\nLock Time: {locktime} ({locktimeinunix})\nUnlock Time: {unlocktime} ({unlocktimeinunix})')

bot.run(TOKEN)
