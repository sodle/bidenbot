import os
import sys
import logging
import json
from slackeventsapi import SlackEventAdapter
from slack import WebClient
from flask import Flask

import bidenbot

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))

if 'SLACK_SIGNING_SECRET' in os.environ:
    SLACK_SIGNING_SECRET = os.environ['SLACK_SIGNING_SECRET']
else:
    SLACK_SIGNING_SECRET = bidenbot.get_secret('/Biden/SlackSigningSecret')
if 'SLACK_ACCESS_TOKEN' in os.environ:
    SLACK_ACCESS_TOKEN = os.environ['SLACK_ACCESS_TOKEN']
else:
    SLACK_ACCESS_TOKEN = bidenbot.get_secret('/Biden/SlackAccessToken')

app = Flask(__name__)

slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, '/biden/slack/events', app)
slack_client = WebClient(token=SLACK_ACCESS_TOKEN)


@slack_events_adapter.on('app_mention')
def on_message(payload):
    print(json.dumps(payload, indent=2))
    mention = f"<@{payload['event']['user']}>"
    channel = payload['event']['channel']
    slack_client.chat_postMessage(channel=channel, text=f'{mention} {bidenbot.get_random_tweet()}')


if __name__ == '__main__':
    app.run()
