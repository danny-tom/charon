#! /bin/bash

# Kill the running processes of tmux if present
if pgrep python3
then
    echo $(sudo pkill python3)
fi
