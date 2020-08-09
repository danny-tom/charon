#! /bin/bash
set -euo pipefail

# Kill the running processes of tmux if present
chmod +x $(dirname "$0")/kill-bot.sh
sh $(dirname "$0")/kill-bot.sh

# Install the dependencies
pip3 install -U pip setuptools

if ! pip3 list | grep python-dotenv 
then
    echo $(python3 -m pip install --user python-dotenv)
fi

if ! pip3 list | grep discord.py
then
    echo $(python3 -m pip install --user discord.py)
fi

# Replace the TOKEN with our secret
sed -i "s/###TOKEN HERE###/$PRODUCTION_TOKEN/g" .env

# Run the daemon
sudo systemctl list-units --type service -all
