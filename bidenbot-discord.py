import os
import sys
import logging
from typing import Union
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


async def respond_to(message: discord.Message, target: Union[str, None] = None):
    tweet = bidenbot.get_random_tweet()
    if target is None:
        try:
            await message.reply(content=tweet, mention_author=False)
        except discord.DiscordException as e:
            logger.error(e)
    else:
        try:
            await message.channel.send(f"{target} {tweet}")
        except discord.DiscordException as e:
            logger.error(e)


@client.event
async def on_ready():
    logger.info(f'Logged in as {client.user}.')


@client.event
async def on_message(message: discord.Message):
    username = message.author.display_name

    mentions = message.mentions
    biden_mentioned = False
    if len(mentions) > 0:
        if mentions[0].mention == client.user.mention:
            biden_mentioned = True
            mentions = mentions[1:]

    if message.content.lower().startswith('!biden') or biden_mentioned:
        if len(mentions) > 0:
            for user in message.mentions:
                logger.info(f'{username} set Biden upon {user.name}!')
                await respond_to(message, target=user.mention)
        else:
            logger.info(f'{username} provoked Biden!')
            await respond_to(message)
    else:
        roll = bidenbot.roll_d20(with_disadvantage=False)
        logger.info(f'{username} rolled {roll}, needed >={ROLL_TO_HIT} for a spontaneous insult...')
        if roll >= ROLL_TO_HIT:
            logger.info(f'Spontaneously insulting {username}!')
            await respond_to(message)
        else:
            logger.info(f'{username} avoided a spontaneous insult!')


if __name__ == '__main__':
    client.run(DISCORD_TOKEN)
