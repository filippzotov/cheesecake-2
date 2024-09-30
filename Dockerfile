# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install ffmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg

# Install dependencies (yt-dlp, discord.py, PyNaCl, etc.)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Make sure to expose the necessary environment variables for your bot
ENV DISCORD_TOKEN="your_discord_token_here"

# Run the bot
CMD ["python", "bot.py"]
