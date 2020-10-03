import discord
import os
import random
import json
import boto3

ssm = boto3.client('ssm', region_name='us-west-2')
DISCORD_TOKEN = ssm.get_parameter(
    Name='/Biden/DiscordToken', WithDecryption=True)['Parameter']['Value']

client = discord.Client(activity=discord.Game("!biden"))

ROLL_TO_HIT = 20


def roll_d20() -> bool:
    roll = random.randint(1, 20)
    print(f'rolled {roll}')
    return roll >= ROLL_TO_HIT


with open('tweets.json') as tweetfile:
    tweets = json.load(tweetfile)


def get_random_tweet() -> str:
    return random.choice(tweets)


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


@client.event
async def on_message(message):
    if message.content == '!biden' or roll_d20():
        await message.channel.send(f"{message.author.mention} {get_random_tweet()}")

client.run(DISCORD_TOKEN)
