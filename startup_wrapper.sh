#!/bin/bash

# Check if tmux session already exists
SESSION_NAME="my_tmux_session"
tmux has-session -t $SESSION_NAME 2>/dev/null

if [ $? != 0 ]; then
    # Create a new session and run the application
    tmux new-session -d -s $SESSION_NAME "/app/startup.sh"
fi

# Attach to the tmux session
tmux attach-session -t $SESSION_NAME
