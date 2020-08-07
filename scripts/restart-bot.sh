#! /bin/bash
set -euo pipefail

# Kill the running processes of tmux if present
if ! pgrep tmux
then
    echo $(sudo pkill tmux)
fi

# Install the dependencies
pip3 install -U pip setuptools

if ! pip3 list | grep python-dotenv 
then
    echo $(pip3 install --user python-dotenv)
fi

if ! pip3 list | grep discord.py
then
    echo $(pip3 install --user discord.py)
fi

# Replace the TOKEN with our secret
sed "s/###TOKEN HERE###/$PRODUCTION_TOKEN/g" .env

# Start new tmux and run the process
tmux new -d
tmux send-keys -t 0 "python3 charon.py" ENTER
