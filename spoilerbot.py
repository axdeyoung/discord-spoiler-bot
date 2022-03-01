from typing import List
import discord
from os import path
from argparse import ArgumentParser
import sys
import shlex
from botstate import *

triggerChar = '$'


# Get command responses dir path
wd = path.abspath(__file__)
wd = path.dirname(wd)
commandResponseDir = path.join(wd, "command_responses")

stateFile = path.join(wd, "bot_state")
botState = BotState(stateFile)

# Set up script arg parser
scriptParser = ArgumentParser(description='''Discord Bot to help reign in spoilers on your server''')
scriptParser.add_argument('-t', '--token', metavar='tokenFile', dest='tokenFile', type=str, nargs=1, default=None, required=True,
                        help = "file to load OAuth2 token from")
args = scriptParser.parse_args()                        

# get the Discord client
client = discord.Client()


### HELPERS ###
def parseMessage(message:str):
    '''Reads the Discord message and returns a list of arguments'''
    # test of this message is a valid command
    if not message.startswith(triggerChar):
        return None

    print("Parsing message: {}".format(message))
    slicedMessage = message[1:] # delete the trigger symbol
    parsedMessage = shlex.split(slicedMessage)
    print("Parsed: {}".format(parsedMessage))
    return parsedMessage

def getCommandResponse(fileName:str):
    '''
    Expects a file name in command_responses directory.
    Returns: the string contained in the specified file
    Returns: None if the specified file is not found
    '''

    # append .txt if it doesn't end with .txt already
    if not fileName.endswith(".txt"):
        fileName = fileName + ".txt"
    
    # grab the contents of the file
    filePath = path.join(commandResponseDir, fileName)
    try:
        with open(filePath, "r") as file:
            fileContents = file.read()
        # return the contents of the file
        return fileContents
    except:
        return None


### COMMAND RESPONSES ###
async def respondHelp(message:discord.Message, commandArgs:List[str]):
    if len(commandArgs) == 1: # if help used on its own
        print("Sending basic help text")
        response = getCommandResponse("help")
        await message.channel.send(response)
    else: # if one or more arguments are passed to help
        print("Attempting to send help text for {}".format(commandArgs[1]))
        # get help file of format "help_cmd.txt"
        response = getCommandResponse("help_{}".format(commandArgs[1].lower()))
        # if that message doesn't exist, give generic command not found text
        if response == None:
            response = getCommandResponse("not_found").format("help text for", commandArgs[1].lower())
        await message.channel.send(response)

async def respondCommandNotFound(message:discord.message, commandArgs:List[str]):
    response = getCommandResponse("not_found").format("command", commandArgs[0].lower())
    await message.channel.send(response)

async def listMedia(message:discord.message, commandArgs:List[str]):

    if len(botState.roles) == 0:
        response = getCommandResponse("listmedia_empty")
    else:
        response = getCommandResponse("listmedia_header").format(triggerChar)
        response = response + "```"
        for roleID in botState.roles:
            roleName = message.guild.get_role(roleID).name
            response = response + "\n" + roleName
        response = response + "```"

    await message.channel.send(response)


async def addMedia(message:discord.message, commandArgs:List[str]):
    response = None
    try:
        mediaName = commandArgs[1]
    except:
        response = getCommandResponse("help_addmedia")
        await message.channel.send(response)
        return

    response = getCommandResponse("addmedia").format(mediaName)
    if not await botState.addRole(mediaName, message.guild):
        response = getCommandResponse("already_exists").format("role", mediaName)

    await message.channel.send(response)


async def deleteMedia(message:discord.message, commandArgs:List[str]):
    response = None
    
    try:
        mediaName = commandArgs[1]
    except:
        response = getCommandResponse("help_deletemedia")
        await message.channel.send(response)
        return

    response = getCommandResponse("deletemedia").format(mediaName)
    role = discord.utils.get(message.guild.roles, name=mediaName)
    if not await botState.deleteRole(role):
        response = getCommandResponse("not_found").format("media role", mediaName)

    await message.channel.send(response)
        

### EVENT HANDLERS ###
@client.event
async def on_ready():
    print("Logged in as user {0.user} and ready to go!".format(client))

    # TODO: check voice state and ping channel users

@client.event
async def on_message(message:discord.Message):
    # if the message is from me, ignore it.
    if message.author == client.user:
        return 
    # if the message is not a command, ignore it
    if not message.content.startswith(triggerChar):
        return

    # read message
    commandArgs = parseMessage(message.content)

    # respond to valid commands
    command = commandArgs[0].lower()

    if command == "ping":
        print("Ponging!")
        await message.channel.send('pong')
    
    elif command == "help" or command == "h":
        await respondHelp(message, commandArgs)

    elif command == "listmedia" or command == "l":
        await listMedia(message, commandArgs)

    elif command == "unspoil":
        await message.channel.send("unspoil not yet implemented")
        #TODO implement this

    elif command == "spoil":
        await message.channel.send("spoil not yet implemented")
        #TODO implement this

    elif command == "addmedia" and message.author.guild_permissions.manage_roles:
        await addMedia(message, commandArgs)
    
    elif command == "deletemedia" and message.author.guild_permissions.manage_roles:
        await deleteMedia(message, commandArgs)
    # TODO: add a bunch more commands and stuff
    else:
        await respondCommandNotFound(message, commandArgs)

@client.event
async def on_voice_state_update(member:discord.Member, before:discord.VoiceState, after:discord.VoiceState):
    print("{0.display_name} updated their voice state".format(member))



### MAIN ###
def main():
    # get the token file path from argument parser
    tokenPath = args.tokenFile[0]

    # open and read the token file. 
    # Format is expected to be the token with any amount of leading or trailing whitespace.
    with open(tokenPath, 'r') as tokenFile:
        token = tokenFile.read().strip()

    # Finally, start the client
    client.run(token)

# wrapping my code in a main function makes the C programmer in me feel safe.
sys.exit(main())