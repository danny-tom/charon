#! /bin/sh

# Kill the running processes of tmux if present
if pgrep tmux
then
    sudo pkill tmux
fi

# Install the dependencies
if pip3 list | grep python3-dotenv
then
    pip3 install python-dotenv 
fi

if  pip3 list | grep discord.py
then
    pip3 install discord.py
fi

# Clone the repository
git clone https://https://github.com/danny-tom/charon.git
cd charon

# Replace the TOKEN with our secret
sed -i's/###TOKEN HERE###/{PRODUCTION_TOKEN}/g' .env

# Start new tmux and run the process
tmux new -d
tmux send-keys -t 0 "python3 charon.py" ENTER
