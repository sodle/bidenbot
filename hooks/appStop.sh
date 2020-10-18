#!/usr/bin/env bash
set -e

if systemctl is-active bidenbot-discord; then
  systemctl stop bidenbot-discord
fi
if systemctl is-active bidenbot-slack; then
  systemctl stop bidenbot-slack
fi
