import discord
from discord.ext import commands
import os
import sqlite3
import random
import string
import asyncio

intents = discord.Intents.default()
intents.message_content = True  # This enables your bot to read messages

bot = commands.Bot(command_prefix='!', intents=intents)
channel = None  # Initialize channel as None
DB_NAME = "confessions.db"

def connect_db():
    conn = sqlite3.connect(DB_NAME)
    return conn

@bot.event
async def on_ready():
    global channel
    # Ensure the bot is ready and the channel is fetched
    channel_id = 1339294365360717864  # Replace with your actual channel ID
    channel = bot.get_channel(channel_id)
    
    if channel is None:
        print(f"Error: Could not find channel with ID {channel_id}")
    else:
        print(f"Bot has connected to the channel {channel.name}!")

@bot.command(name='confess')
async def confess(ctx, uid: str):
    if channel is None:
        await ctx.send("Error: Bot channel is not available. Please try again later.")
        return

    conn = connect_db()
    cursor = conn.cursor()
    
    # Check if the confession with the given ID exists
    cursor.execute("SELECT * FROM confessions WHERE id = ?", (uid,))
    result = cursor.fetchone()
    
    if result is None:
        # If no such confession exists
        await ctx.send(f"Incorrect ID, no such confession exists.")
    else:
        # If a confession exists, retrieve the details
        confession_id = result[0]  # Unique ID
        message = result[1]  # Confession message
        file_path = result[2]  # File path (if any)

        # Create an embed for the confession
        embed = discord.Embed(
            title=f"Confession (#{confession_id})",
            description=message,
            color=discord.Color.purple()  # You can choose any color you like
        )

        # If there's a file, send it with the embed
        if file_path:
            # Open the file and send it as an attachment
            with open(file_path, 'rb') as file:
                await channel.send(embed=embed, file=discord.File(file, filename=os.path.basename(file_path)))
        else:
            # If no file is attached, just send the embed
            await channel.send(embed=embed)

    conn.close()

def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    bot.run(os.getenv("TOKEN"))
