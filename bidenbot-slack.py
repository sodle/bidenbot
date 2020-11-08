import os
import sys
import logging
import json
import time
import threading
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

def send_message(channel: str, text: str, thread_ts: str = None, delay_sec: int = 0):
    time.sleep(delay_sec)
    slack_client.chat_postMessage(channel=channel, text=text, thread_ts=thread_ts)


@slack_events_adapter.on('app_mention')
def on_message(payload):
    logger.info(json.dumps(payload))

    user_target = payload['event']['user']

    mentioned_users = [e for e in payload['event']['blocks'][0]['elements'][0]['elements']
                       if e['type'] == 'user' and e['user_id'] != payload['authorizations'][0]['user_id']]
    logger.info(json.dumps(mentioned_users))
    if len(mentioned_users) > 0:
        user_target = mentioned_users[0]['user_id']

    target_profile = slack_client.users_info(user=user_target)
    logger.info(target_profile)

    mention = f"<@{user_target}>"

    channel = payload['event']['channel']

    send_thread = threading.Thread(target=send_message, kwargs={
        'channel': channel,
        'text': f'{mention} {bidenbot.get_random_tweet()}',
        'thread_ts': payload['event'].get('thread_ts', None),
        'delay_sec': 300 if target_profile['user']['is_bot'] else 0
    })
    send_thread.run()


if __name__ == '__main__':
    app.run()
