import json
import discord
from discord.ext import commands
from discord.ui import View, Button
from dotenv import load_dotenv
import os,logging

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
bot = commands.Bot(command_prefix="!", intents=intents)

# Your target channel ID
TARGET_CHANNEL_ID = CHANNELID  # Replace with your channel ID

class DynamicView(discord.ui.View):
    try:
        def __init__(self, options, previous_selection=None):
            super().__init__(timeout=None)
            self.options = options
            self.previous_selection = previous_selection

            # Add buttons for each option with numbers
            for i, option in enumerate(options, start=1):
                button = Button(label=str(i), custom_id=str(i),style=discord.ButtonStyle.blurple)
                button.callback = self.create_callback(i, option)
                self.add_item(button)

            # Add "Back to Main Menu" button
            back_button = Button(label="Back to Main Menu", style=discord.ButtonStyle.red, custom_id="back")
            back_button.callback = self.back_to_main_menu
            self.add_item(back_button)
            
    except Exception as e:
        logging.info(f"{e} --- failed Init")
    
    
    try:
        def create_callback(self, index, option):
            async def callback(interaction: discord.Interaction):
                next_options = menu_data.get(option)
                if isinstance(next_options, list):
                    # Show the next set of options with numbers
                    options_text = "\n".join([f"{i}. {opt}" for i, opt in enumerate(next_options, start=1)])
                    embed = discord.Embed(title=f"Select an option from:\n\n",description=options_text, color=discord.Color.blue())

                    await interaction.response.send_message(embed=embed, view=DynamicView(next_options, option))
                else:
                    # Show the final message
                    await interaction.response.send_message(content=f'{option}\n\n {next_options}')
            return callback
        
    except Exception as e:
        logging.info(f"{e} --- callback failed")
    
       
    async def back_to_main_menu(self, interaction: discord.Interaction):
        try:             
            options_text = "\n".join([f"{i}. {opt}" for i, opt in enumerate(menu_data['menu'], start=1)])
            embed = discord.Embed(title=f"Choose an option:\n\n",description=options_text, color=discord.Color.blue())

            await interaction.response.send_message(embed=embed, view=DynamicView(menu_data['menu']))
        except Exception as e:
            logging.info(f"{e} --- back to main menu failed")
            pass
       

@bot.event
async def on_ready():
    try:
        logging.info(f'Logged in as {bot.user}')

        channel = bot.get_channel(TARGET_CHANNEL_ID)
        if channel:
            # Show initial options
            options_text = "\n".join([f"{i}. {opt}" for i, opt in enumerate(menu_data['menu'], start=1)])
            embed = discord.Embed(title=f"Hey Im happy to assist you...\nPlease choose an option below:\n\n",description=options_text, color=discord.Color.blue())

            await channel.send(embed=embed,view=DynamicView(menu_data['menu']))
            # await channel.send(f"Choose an option:\n\n{options_text}", view=DynamicView(menu_data['menu']))
        else:
            logging.info(f"Channel with ID {TARGET_CHANNEL_ID} not found")
            
    except Exception as e:
        logging.info(f"Bot ready failed --- {e}")
        pass
    
    

bot.run(DISCORD_TOKEN)
