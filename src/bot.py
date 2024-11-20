import os
import discord

TOKEN = os.getenv('SPICYBOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

async def do_quote_message(
    channel: discord.TextChannel,
    quote: str,
    user: discord.User,
    quoter: discord.User,
    jump_url: str = None
):
    message = f'> {quote}\n'
    message += f'-{user.mention} '
    message += f'*(quoted by: {quoter.mention})*'
    if jump_url is not None:
        message += f'\n{jump_url}'

    await channel.send(
        content=message,
        allowed_mentions=discord.AllowedMentions(everyone=False)
    )

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
    quoter = interaction.user
    if quotes_channel is None:
        await interaction.response.send_message('Error: No quotes channel in guild!', ephemeral=True)
    else:
        try:
            await do_quote_message(quotes_channel, quote, user, quoter)
            await interaction.response.send_message('Success!', ephemeral=True)
        except discord.errors.Forbidden:
            await interaction.response.send_message(
                f'Error: Bot does not have permission to send messages in {quotes_channel.mention}',
                ephemeral=True
            )

@tree.context_menu(
    name='Quote Message'
)
async def quote_message(interaction: discord.Interaction, message: discord.Message):
    user = message.author
    quote = message.content
    quotes_channel: discord.TextChannel = discord.utils.get(
        interaction.guild.channels, name='quotes'
    )
    quoter = interaction.user
    jump_url = message.jump_url
    if quotes_channel is None:
        await interaction.response.send_message('Error: No quotes channel in guild!', ephemeral=True)
    else:
        try:
            await do_quote_message(quotes_channel, quote, user, quoter, jump_url)
            await interaction.response.send_message('Success!', ephemeral=True)
        except discord.errors.Forbidden:
            await interaction.response.send_message(
                f'Error: Bot does not have permission to send messages in {quotes_channel.mention}',
                ephemeral=True
            )


client.run(TOKEN)
