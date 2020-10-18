import os
import sys
import logging
import discord

import bidenbot

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))

# Fetch the Discord bot token from either environment variables or else AWS SSM
if 'DISCORD_TOKEN' in os.environ:
    DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
else:
    DISCORD_TOKEN = bidenbot.get_secret('/Biden/DiscordToken')

# d20 roll needed to respond to a non-"!biden" message
ROLL_TO_HIT = int(os.environ.get('ROLL_TO_HIT', 20))

client = discord.Client(activity=discord.Game("!biden"))


async def respond_to(message: discord.Message):
    try:
        await message.channel.send(f"{message.author.mention} {bidenbot.get_random_tweet()}")
    except discord.DiscordException as e:
        logger.error(e)


@client.event
async def on_ready():
    logger.info(f'Logged in as {client.user}.')


@client.event
async def on_message(message: discord.Message):
    mention = message.author.display_name
    if message.content.lower().startswith('!biden'):
        logger.info(f'{mention} provoked Biden!')
        await respond_to(message)
    else:
        roll = bidenbot.roll_d20()
        logger.info(f'{mention} rolled {roll}, needed >={ROLL_TO_HIT} for a spontaneous insult...')
        if roll >= ROLL_TO_HIT:
            logger.info(f'Spontaneously insulting {mention}!')
            await respond_to(message)
        else:
            logger.info(f'{mention} avoided a spontaneous insult!')


client.run(DISCORD_TOKEN)
