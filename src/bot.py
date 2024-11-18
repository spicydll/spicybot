import os
import discord

TOKEN = os.getenv('SPICYBOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


@client.event
async def on_ready():
    await tree.sync()
    print("Tree sync complete")

@tree.command(
    name='quote',
    description='Make a quote of a user in the designated quotes channel'
)
@discord.app_commands.describe(
    user='The user you are quoting',
    quote='The bars they be spittin'
)
async def quote_cmd(interaction: discord.Interaction, user: discord.User, quote: str):
    quotes_channel: discord.TextChannel = discord.utils.get(
        interaction.guild.channels, name='quotes'
    )
    await quotes_channel.send(f'"{quote}"\n-{user.mention}')
    await interaction.response.send_message('Success (probably)!')

client.run(TOKEN)
