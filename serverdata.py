### ServerData class manages data for a single server
# needs to be picklable
class ServerData:
    """docstring for ServerData"""

    # members:
        # roles: a list of strings; names of roles managed by the bot
        # channel: bot's home channel. This is where the bot will update the voice channel

    def __init__(self):

# TODO: determine how roles can be represented by the discord api