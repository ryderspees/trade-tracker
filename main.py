from urllib import response
import discord
from discord import app_commands
import datetime
import discord.ext.tasks
import request

TOKEN = '' # Hidden for security

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

    # check to see if 10am call is on a Monday 
    if datetime.datetime.today().weekday() == 0:
        # past 7 days
        past = datetime.datetime.now() - datetime.timedelta(days=7)
        data = request.fetch_data()

        if data == False:
            return

        # loop each channel added from users
        for channel in channels:
            responseMessage = "--------**Weekly Breakdown**--------\n"# new

            # make each valid trade look pretty
            for trade in data:
                disclosed_date = datetime.datetime.strptime(trade['disclosure_date'], "%m/%d/%Y")
                if disclosed_date > past:
                    if (trade['ticker'] != '--'):
                        responseMessage += ('Name: ' + str(trade['senator']) + '\n'
                            + 'Stock Ticker: ' + str(trade['ticker']) + '\n'
                            + 'Transaction Type: ' + str(trade['type']) + '\n'
                            + 'Amount: ' + str(trade['amount']) + '\n'
                            + 'Disclosure Date: ' + str(trade['disclosure_date']) + '\n'
                            + 'Transaction Date: ' + str(trade['transaction_date']) + '\n'
                            + '----------------------------------------\n')
            await channel.send(responseMessage)



@client.event
async def on_guild_join(guild):
    channel = guild.channels[0].text_channels[0]
    await channel.send("**Thanks for adding me to your server!**\n\nTo start, type `/track` and enter the channel you would like updates in\n\nFor other commands, type `/help`")
    

@tree.command(name = "track", description = "Starts tracking Senate trades in specified channel", guild = discord.Object(id=1004942542820876348))
async def self(interaction: discord.Interaction, channel : discord.TextChannel):
    channels.append(channel)
    if not called_once_a_week.is_running():
        called_once_a_week.start()
        print("Weekly task started in server " + interaction.guild.name + " with ID " + str(interaction.guild.id))
    await interaction.response.send_message(f"{interaction.user.name}, this server will now receive a weekly report of Senate stock trading in <#{channel.id}> on Mondays at 10am EST")
    

client.run(TOKEN)
