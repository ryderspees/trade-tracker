import discord
from discord import app_commands
import datetime
import discord.ext.tasks

TOKEN = 'MTAwNDk0MTM0NzUzNjUxMTAzNg.GpyTo8.uQNkSeVnsDRbydGey6H_IQwDoWivuvl9XfcUXM'

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=discord.Object(id=1004942542820876348))
            self.synced = True
        print('We have logged in as {0.user}'.format(client))



client = aclient()
tree = app_commands.CommandTree(client)
channels = []
timeToRun = datetime.time(hour=14, minute=0, second=0)

@discord.ext.tasks.loop(time=timeToRun)
async def called_once_a_week():
    await client.wait_until_ready()
    if datetime.datetime.today().weekday() == 0:
        for channel in channels:
            await channel.send("ITS 10AM ON MONDAY")


@client.event
async def on_guild_join(guild):
    channel = guild.channels[0].text_channels[0]
    await channel.send("**Thanks for adding me to your server!**\n\nTo start, type `/track` and enter the channel you would like updates in\n\nFor other commands, type `/help`")
    
@tree.command(name = "track", description = "Starts tracking Senate trades in specified channel", guild = discord.Object(id=1004942542820876348))
async def self(interaction: discord.Interaction, channel : discord.TextChannel):
    channels.append(channel)
    if not called_once_a_week.is_running():
        called_once_a_week.start()
        print("Weekly task started")
    await interaction.response.send_message(f"{interaction.user.name}, this server will now receive a weekly report of senator trading in `#{channel.name}` on Mondays at 10am EST")

@tree.command(name = "pelosiattack", description = "Run it, I dare you", guild = discord.Object(id=1004942542820876348))
async def attack(interaction: discord.Interaction, channel : discord.VoiceChannel):
    # connects to vc
    vc = await channel.connect()

    # moves everyone to channel
    for v in interaction.guild.voice_channels:
        for member in v.members:
            await member.move_to(channel)

    # mutes all
    for v in interaction.guild.voice_channels:
        for member in v.members:
            if member.bot == False:
                await member.edit(mute=True)

    # <3
    await interaction.response.send_message(f"help me", tts=True)

    await vc.disconnect()

client.run(TOKEN)
