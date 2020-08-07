#! /bin/sh

# Kill the running processes of tmux if present
if pgrep tmux
then
    echo sudo pkill tmux
fi

# Install the dependencies
if pip3 list | grep python3-dotenv
then
    echo $(pip3 install python-dotenv)
fi

if  pip3 list | grep discord.py
then
    echo $(pip3 install discord.py)
fi

# Clone the repository
echo $(git clone https://github.com/danny-tom/charon.git)
echo $(cd charon)

# Replace the TOKEN with our secret
echo $(sed -i 's/###TOKEN HERE###/${TEST_TOKEN}/g' .env)

# Start new tmux and run the process
echo $(tmux new -d)
echo $(tmux send-keys -t 0 "python3 charon.py" ENTER)
