
import discord
import pickle

### GuildData class manages data for a single server
# needs to be picklable
class BotState:
    """docstring for BotState"""

    # members:
        # roles: list of discord.Role.id ints; roles managed by the bot
        # channelDict: a Dictionary of (discord.Guild.id : discord.TextChannel.id); home channel in each guild
        # saveFileName: str; 

    def __init__(self, saveFileName:str):
        self.roles = list()
        self.channelDict = dict()
        self.saveFileName = saveFileName
        try:
            with open(saveFileName, "rb") as file:
                loaded = pickle.load(file)
                self.roles = loaded.roles
                self.channelDict = loaded.channelDict
            print("Loaded bot state from {0}".format(saveFileName))
        except:
            print("Created new bot state to be saved as {0}".format(saveFileName))

    def save(self):
        with open(self.saveFileName, "wb") as file:
            pickle.dump(self, file)


    async def addRole(self, roleName:str, guild:discord.Guild):
        '''
        Creates a role on the specified guild if one with the given name doesn't already exist
        Returns: True if the role was created successfully
        Returns: False if the role already exists
        '''
        if discord.utils.get(guild.roles, name=roleName) == None:
            role = await guild.create_role(name=roleName, colour=0x000000, mentionable=True)
            self.roles.append(role.id)
            self.save()
            return True
        else:
            return False

    async def deleteRole(self, role:discord.Role):
        '''
        Returns True if role successfully deleted
        Returns False if role is not managed
        '''
        # the order of the following two remove/delete are important
        # if the role was deleted on Discord, it will automatically
        # sync the bot state with the Discord state
        try:
            # first try to remove the role from the bot state
            self.roles.remove(role.id)
            self.save()

            # if the role was successfully removed from the bot state, try to delete the role from Discord
            await role.delete()
        except:
            return False
        return True
        

    def registerChannel(self, channel:discord.TextChannel):
        self.channelDict[channel.guild.id] = channel.id
        self.save()

    def unregisterChannel(self, guild:discord.Guild):
        self.channelDict.pop(guild.id)
        self.save()



# TODO: determine how roles can be represented by the discord api