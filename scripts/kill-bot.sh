#! /bin/bash

# Kill the running processes of tmux if present
if ! pgrep tmux
then
    echo $(sudo pkill tmux)
fi
