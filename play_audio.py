import discord
import yt_dlp
import asyncio


async def play_youtube_audio(voice_client: discord.VoiceClient, url: str):
    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "quiet": True,  # Reduce output
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        audio_url = info_dict["url"]

    # Play the audio stream using FFmpeg
    if not voice_client.is_playing():
        ffmpeg_options = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn",  # Disable video
        }
        voice_client.play(discord.FFmpegPCMAudio(audio_url, **ffmpeg_options))

        # Wait while the audio is playing
        while voice_client.is_playing():
            await asyncio.sleep(1)
    else:
        print("Bot is already playing audio.")
