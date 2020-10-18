from pathlib import Path
import json
import random
import boto3

tweets_path = Path(__file__).parent.joinpath('tweets.json')

with open(tweets_path) as tweetfile:
    tweets = json.load(tweetfile)


def get_random_tweet() -> str:
    return random.choice(tweets)


def roll_d20() -> int:
    roll = random.randint(1, 20)
    return roll


def get_secret(path: str) -> str:
    ssm = boto3.client('ssm', region_name='us-west-2')
    return ssm.get_parameter(Name=path, WithDecryption=True)['Parameter']['Value']
