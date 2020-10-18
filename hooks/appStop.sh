#!/usr/bin/env bash
set -e

# Clean up the legacy unit file if it exists
if systemctl is-active biden; then
  systemctl stop biden
fi
rm -rf /etc/systemd/system/bidenbot-discord.service

# Stop the new 2nd gen unit files if we've already migrated
if systemctl is-active bidenbot-discord; then
  systemctl stop bidenbot-discord
fi
