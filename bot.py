import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from play_audio import play_youtube_audio
import asyncio

# Load the environment variables from the .env file
load_dotenv()

# Get the token from the environment
TOKEN = os.getenv("DISCORD_TOKEN")

# Define intents
intents = discord.Intents.default()
intents.message_content = True  # Ensure the bot can read messages

# Define the command prefix and pass the intents
bot = commands.Bot(command_prefix="*", intents=intents)

# A dictionary to store the queues for each guild (server)
queues = {}


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


async def play_next_in_queue(ctx):
    """Play the next song in the queue, if any"""
    if queues[ctx.guild.id]:
        next_url = queues[ctx.guild.id].pop(0)
        voice_client = ctx.voice_client
        success = await play_youtube_audio(voice_client, next_url)

        # Check if there are more items in the queue
        if queues[
            ctx.guild.id
        ]:  # If there are more songs in the queue, play the next song
            await play_next_in_queue(ctx)
        else:
            await ctx.send("Queue is empty, disconnecting...")
            await voice_client.disconnect()
    else:
        await ctx.send("Queue is empty.")


@bot.command(name="play", help="Plays audio from a YouTube video in a voice channel.")
async def play(ctx, url: str):
    # Initialize the queue for the guild if it doesn't exist
    if ctx.guild.id not in queues:
        queues[ctx.guild.id] = []

    if ctx.author.voice:
        voice_channel = ctx.author.voice.channel

        # Check if the bot is already connected to a voice channel in this guild
        if ctx.voice_client is None:
            # Connect to the voice channel
            voice_client = await voice_channel.connect()
        else:
            voice_client = ctx.voice_client

        # Add the URL to the queue
        queues[ctx.guild.id].append(url)

        # If nothing is playing, start playing the song immediately
        if not voice_client.is_playing():
            await play_next_in_queue(ctx)
        else:
            await ctx.send(f"Added to the queue. Position: {len(queues[ctx.guild.id])}")
    else:
        await ctx.send("You need to be in a voice channel to use this command!")


@bot.command(
    name="stop",
    help="Stops the currently playing audio and disconnects from the voice channel.",
)
async def stop(ctx):
    # Check if the bot is connected to a voice channel in this guild
    if ctx.voice_client:
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()  # Stop the audio playback
        queues[ctx.guild.id] = []  # Clear the queue
        await ctx.voice_client.disconnect()  # Disconnect the bot from the voice channel
        await ctx.send("Stopped the audio and cleared the queue.")
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command(
    name="skip", help="Skips the currently playing audio and plays the next in queue."
)
async def skip(ctx):
    # Check if the bot is connected to a voice channel in this guild
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()  # Stop the current audio
        await ctx.send("Skipping to the next song...")

        # Play the next song in the queue if available
        if queues[ctx.guild.id]:
            await play_next_in_queue(ctx)
        else:
            await ctx.send("No more songs in the queue, disconnecting...")
            await ctx.voice_client.disconnect()
    else:
        await ctx.send("No audio is currently playing.")


# Run the bot using the token from the environment
bot.run(TOKEN)
