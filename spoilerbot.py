import discord
import pickle
from os import path
from argparse import ArgumentParser

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

    if message.content.startswith("$kill"):
        exit()

def main():
    # run initialization stuff

    # parentDir = path.dirname(path.abspath(__file__))
    # tokenFileName = path.join(parentDir, "token")

    parser = ArgumentParser(description='''Discord Bot to help reign in spoilers on your server''')
    parser.add_argument('-t', '--token', metavar='tokenFile', dest='tokenFile', type=str, nargs=1, default=None, required=True,
                        help = "file to load OAuth2 token from")

    args = parser.parse_args()

    tokenPath = args.tokenFile[0]

    with open(tokenPath, 'r') as tokenFile:
        token = tokenFile.read().strip()

    client.run(token)

sys.exit(main())