import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from play_audio import play_youtube_audio

# Load the environment variables from the .env file
load_dotenv()

# Get the token from the environment
TOKEN = os.getenv("DISCORD_TOKEN")

# Define intents
intents = discord.Intents.default()
intents.message_content = True  # Ensure the bot can read messages

# Define the command prefix and pass the intents
bot = commands.Bot(command_prefix="*", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command(name="play", help="Plays audio from a YouTube video in a voice channel.")
async def play(ctx, url: str):
    if ctx.author.voice:
        voice_channel = ctx.author.voice.channel

        # Check if the bot is already connected to a voice channel in this guild
        if ctx.voice_client is None:
            # Connect to the voice channel
            voice_client = await voice_channel.connect()
        else:
            voice_client = ctx.voice_client

        # Play the audio from the YouTube video using the separate function
        await play_youtube_audio(voice_client, url)

    else:
        await ctx.send("You need to be in a voice channel to use this command!")


@bot.command(
    name="stop",
    help="Stops the currently playing audio and disconnects from the voice channel.",
)
async def stop(ctx):
    # Check if the bot is connected to a voice channel in this guild
    if ctx.voice_client:  # ctx.voice_client is the VoiceClient instance for the guild
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()  # Stop the audio playback
        await ctx.voice_client.disconnect()  # Disconnect the bot from the voice channel
        await ctx.send("Stopped the audio and disconnected from the voice channel.")
    else:
        await ctx.send("The bot is not connected to a voice channel.")


# Run the bot using the token from the environment
bot.run(TOKEN)
