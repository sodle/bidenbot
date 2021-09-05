#!/usr/bin/env bash
set -e

systemctl daemon-reload
#systemctl start bidenbot-discord
systemctl start bidenbot-slack
