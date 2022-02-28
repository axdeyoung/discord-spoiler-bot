import discord
import pickle

client = discord.Client()

@client.event
async def on_ready():
    print("Logged in as user {0.user}".format(client))

@client.event
async def on_message(message):
    # if the message is from me, ignore it.
    if message.author == client.user:
        return 

    if message.content.startswith("$ping"):
        await message.channel.send("pong")


# run initialization stuff

client.run('OTQ3NzAwOTU5NTg3NDcxNDMx.YhxFTA.z6IFmoWeia0Adz-24ArJZFRAaQo')