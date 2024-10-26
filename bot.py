import discord
import random
import asyncio
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Global variable to store the target channel ID and control the message loop
target_channel_id = None
send_random = False

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(f"Error syncing commands: {e}")

# Slash command to set the target channel
@bot.tree.command(name="ch", description="Set a channel to send random 0 or 1 messages")
async def set_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    global target_channel_id, send_random
    target_channel_id = channel.id
    send_random = True  # Start sending messages

    await interaction.response.send_message(f"Bot will start sending random 0 or 1 in {channel.mention}")

    # Start the random message loop
    await start_sending_random()

async def start_sending_random():
    global send_random
    while send_random:
        channel = bot.get_channel(target_channel_id)
        if channel:
            await channel.send(str(random.choice([0, 1])))
        await asyncio.sleep(1)  # 1-second cooldown between messages

@bot.tree.command(name="stop", description="Stop sending random 0 or 1 messages")
async def stop_sending(interaction: discord.Interaction):
    global send_random
    send_random = False  # Stop sending messages
    await interaction.response.send_message("Stopped sending random 0 or 1 messages.")

bot.run(TOKEN)
