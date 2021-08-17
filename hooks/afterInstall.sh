#!/usr/bin/env bash
set -e

systemctl disable bidenbot-discord
systemctl enable bidenbot-slack
