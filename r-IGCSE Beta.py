import os
from typing import Any, Coroutine, Optional
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
	await bot.change_presence(activity=discord.Game(name="Fortnite"))

@bot.event
async def on_message(message:discord.Message):
    message_channel = message.channel.id
    message_content = message.content
    if message_channel == 1153283974211321906:
        if message.author.bot: 
            print(message_content)
        else: 
            message.delete()
    else: 
         return

class LockView(discord.ui.View):
  def __init__(self, *, timeout: float, unlocktimeout: float = -1, channelid: discord.TextChannel, unlock = False) -> None:
    super().__init__(timeout=timeout)
    self.channelid = channelid
    self.unlocktime = unlocktimeout
    self.unlock = unlock
    self.msg = f"{'Unl' if unlock else 'L'}ocked channel."

  async def on_timeout(self):
    
    everyonerole = self.guild.get_role(1111128710133854289)

    channel = bot.get_channel(self.channelid)
    overwrite = channel.overwrites_for(everyonerole)
    overwrite.send_messages=self.unlock

    await channel.set_permissions(everyonerole, overwrite=overwrite)
    await channel.send(self.msg)

    if not self.unlock:
      unlockview = LockView(timeout=self.unlocktime, unlock=True, channelid=self.channelid)
      embed = discord.Embed(description=f"Unlocking channel in <t:{int(time.time()) + self.unlocktime}:R>.")
      message = await channel.send(embed=embed, view=unlockview)
      unlockview.message = message
      unlockview.channelid = self.channelid
      unlockview.guild = self.guild
      unlockview.user = self.user


@bot.slash_command(name="channellock", description="locks a channel at a specified time")
async def lockcommand(interaction: discord.Interaction,
                        channelinput: discord.TextChannel =  discord.SlashOption(name="channel_name", description="Which channel do you want to lock?", required=True),
                        locktime: str = discord.SlashOption(name="lock_time", description="At what time do you want the channel to be locked?", required=True),
                        unlocktime: str = discord.SlashOption(name="unlock_time", description="At what time do you want the channel to be unlocked?", required=True)):

  # async def togglechannellock(channelid: discord.TextChannel, msg, lockstatus=True):
  t = int(time.time()) + 1

  try:
    locktime = int(locktime)
    unlocktime = int(unlocktime)
  except ValueError:
    await interaction.send("Times must be (positive) integers.", ephemeral=True)
    return

  if locktime < 0 or unlocktime < 0:
    await interaction.send("Lock time must be positive.", ephemeral=True)
    return
  elif locktime >= unlocktime :
    await interaction.send("Unlock time must be after lock time.", ephemeral=True)
    return
  elif unlocktime < t:
    await interaction.send(f"Unlock time has already passed (current time: {round(time.time())}).", ephemeral=True)
    return


  locktimeinunix = f"<t:{locktime}:F>"
  unlocktimeinunix = f"<t:{unlocktime}:F>"
  await interaction.send(f"<#{channelinput.id}> is scheduled to lock on "
                         f"{locktimeinunix} and unlock on {unlocktimeinunix}", ephemeral=True)
  channelid = f"<#{channelinput.id}>"
  logchannel = bot.get_channel(1153283974211321906)
  await logchannel.send(f'Channel Name: |{channelid}|\n'
                     f'Lock Time: |{locktime}| ({locktimeinunix})\n'
                     f'Unlock Time: |{unlocktime}| ({unlocktimeinunix})')

  view = LockView(timeout=locktime-t, unlocktimeout=unlocktime-max(locktime,t),
                   channelid=channelinput.id)
  embed = discord.Embed(description=f"Locking channel <t:{locktime}:R>.")
  message = await channelinput.send(embed=embed, view=view)
  view.message = message
  view.channel = bot.get_channel(channelid)
  view.guild = interaction.guild
  view.user = interaction.user


bot.run(TOKEN)
