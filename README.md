# BidenBot for Discord

This bot posts random tweets from [@BidenInsultBot](https://twitter.com/bideninsultbot) in Discord.

## Install the hosted version

[Add to Discord](https://discord.com/oauth2/authorize?client_id=761411515903246346&scope=bot)

## Triggers

- Bot responds with an insult whenever someone posts the exact message `!biden`
- 5% chance of responding to any other message

## Development Roadmap

- [x] ~~_Basic insult functionality_~~
- [x] ~~_CICD pipeline_~~
- [X] ~~_Sic Biden on another user with `!biden @JohnSmith#1234`_~~
- [ ] Slack support

# Self-hosting / Development

## Requires

- Python 3.x
- Pipenv
- An AWS account (used to access SSM Parameter Store, a free service)
- A Discord account, with access to the Developer Portal
- A box with outbound HTTP access (tested on Linux)

## Setting up

1. Create an app in the Discord Developer Portal. In the "Bot" tab, enable the bot user and customize it to your liking. Find the "token" and copy it down.
2. In AWS, find the Systems Manager service and its "Parameter Store" tab. Create a new Parameter, with name `/Biden/DiscordToken` and type `SecureString`. For its value, paste the token from step 1, and save the parameter.
3. Configure your local machine or server to access AWS, with a role that enables it to call `ssm:GetParameter` on the parameter you created in step 2.
4. Clone this repo and cd into it.
5. `pipenv install`
6. `pipenv run start`

The bot should now be running and ready to listen for requests. You can message it directly using the Discord username in the "bot" page of the dev portal, or add it to a server using the link:

```
https://discord.com/oauth2/authorize?client_id=<client_id>&scope=bot
```

Where `<client_id>` is found on the "General Information" tab of the discord dev portal.

# Docker
Just use the image.
