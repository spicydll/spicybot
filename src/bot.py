import os
import discord

TOKEN = os.getenv('SPICYBOT_TOKEN')

client = discord.Client()

client.run(TOKEN)
