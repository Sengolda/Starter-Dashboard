import discord
from discord.ext import commands, ipc
import os

SECRET_KEY = open("./config/secretkey.txt", "r").read()
PREFIX = open("./config/prefix.txt", "r").read()
TOKEN = open("./config/token.txt", "r").read()

class client(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ipc = ipc.Server(self, secret_key=SECRET_KEY)

    async def on_ipc_ready(self):
        print("IPC Server Is Ready")

    async def on_ipc_error(self, endpoint, error):
        print(endpoint, "raised", error)

client = client(command_prefix = PREFIX, intents=discord.Intents.all())

@client.ipc.route()
async def get_guild_count(data):
    return len(client.guilds)

@client.ipc.route()
async def get_guild_ids(data):
    final = []
    for guild in client.guilds:
        final.append(guild.id)
    return final    


client.load_extension('cogs.fun')
print('Cog Loaded: Fun')
client.load_extension('cogs.miscellaneous')
print('Cog Loaded: Miscellaneous')
client.load_extension('cogs.moderation')
print('Cog Loaded: Moderation')
client.ipc.start()
client.run(TOKEN)