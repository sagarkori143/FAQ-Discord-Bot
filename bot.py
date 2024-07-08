import json
import discord
from discord.ext import commands
from discord.ui import View, Button
from dotenv import load_dotenv
import os
import logging

# Load environment variables from .env file
load_dotenv()

# Retrieve the bot token and channel ID from the environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNELID = int(os.getenv('CHANNELID'))

# Load the JSON
with open('menu_structure.json', 'r', encoding='utf-8') as file:
    menu_data = json.load(file)

# Initialize the bot
intents = discord.Intents.default()
intents.message_content = True  # Ensure the bot can read message content
bot = commands.Bot(command_prefix="!", intents=intents)

# Your target channel ID
TARGET_CHANNEL_ID = CHANNELID  # Replace with your channel ID

class DynamicView(discord.ui.View):
    def __init__(self, options, user=None, previous_selection=None,**disable):
        super().__init__(timeout=None)
        self.options = options
        self.user = user
        self.previous_selection = previous_selection

        # Add buttons for each option with numbers
        for i, option in enumerate(options, start=1):
            button = Button(label=str(i), custom_id=str(i), style=discord.ButtonStyle.blurple)
            button.callback = self.create_callback(i, option)
            self.add_item(button)

        # Add "Back to Main Menu" button
        if not disable:
            back_button = Button(label="Back to Main Menu", style=discord.ButtonStyle.red, custom_id="back")
            back_button.callback = self.back_to_main_menu
            self.add_item(back_button)

    def create_callback(self, index, option):
        async def callback(interaction: discord.Interaction):
            try:
                if self.user and interaction.user != self.user:
                    await interaction.response.send_message("This interaction is not for you.", ephemeral=True)
                    return

                next_options = menu_data.get(option)
                if isinstance(next_options, list):
                    # Show the next set of options with numbers
                    options_text = "\n".join([f"{i}. {opt}" for i, opt in enumerate(next_options, start=1)])
                    embed = discord.Embed(title=f"Select an option from:\n\n", description=options_text, color=discord.Color.blue())
                    if self.user is None:  # Initial interaction, send DM to user
                        await interaction.user.send(embed=embed, view=DynamicView(next_options, interaction.user))
                        await interaction.response.send_message("Check your DMs for the next options.",ephemeral=True)
                    else:  # Continue interaction in DMs
                        await interaction.response.send_message(embed=embed, view=DynamicView(next_options, interaction.user))
                else:
                    # Show the final message
                    await interaction.response.send_message(content=f'{option}\n\n {next_options}', ephemeral=True)
            except Exception as e:
                logging.error(f"Error in create_callback: {e}")
                await interaction.response.send_message("An error occurred while processing your request.", ephemeral=True)

        return callback

    async def back_to_main_menu(self, interaction: discord.Interaction):
        try:
            if self.user and interaction.user != self.user:
                await interaction.response.send_message("This interaction is not for you.", ephemeral=True)
                return

            options_text = "\n".join([f"{i}. {opt}" for i, opt in enumerate(menu_data['menu'], start=1)])
            embed = discord.Embed(title=f"Choose an option:\n\n", description=options_text, color=discord.Color.blue())
            if isinstance(interaction.channel, discord.DMChannel):
                await interaction.user.send(embed=embed, view=DynamicView(menu_data['menu'], interaction.user))
            else:
                await interaction.followup.send(embed=embed, view=DynamicView(menu_data['menu'], interaction.user))
        except Exception as e:
            logging.error(f"Error in back_to_main_menu: {e}")
            await interaction.response.send_message("An error occurred while processing your request.", ephemeral=True)

@bot.event
async def on_ready():
    try:
        logging.info(f'Logged in as {bot.user}')
        print(f'Logged in as {bot.user}')

        channel = bot.get_channel(TARGET_CHANNEL_ID)
        if channel:
            # Show initial options
            options_text = "\n".join([f"{i}. {opt}" for i, opt in enumerate(menu_data['menu'], start=1)])
            embed = discord.Embed(title=f"Hey I'm happy to assist you...\nPlease choose an option below:\n\n", description=options_text, color=discord.Color.blue())
            await channel.send(embed=embed, view=DynamicView(menu_data['menu'],disable=True))
        else:
            logging.info(f"Channel with ID {TARGET_CHANNEL_ID} not found")
    except Exception as e:
        logging.error(f"Error in on_ready: {e}")

bot.run(DISCORD_TOKEN)

