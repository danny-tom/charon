#! /bin/bash

# Kill the running processes of tmux if present
if pgrep charon.py
then
    echo $(sudo pkill charon.py)
fi
