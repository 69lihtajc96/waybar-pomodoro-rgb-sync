#!/bin/bash

WORK_FLAG="/tmp/pomodoro_work_flag"
BREAK_FLAG="/tmp/pomodoro_break_flag"
PAUSE_FLAG="/tmp/pomodoro_pause_flag"

waybar-module-pomodoro toggle

sleep 0.2

if [ -f "$WORK_FLAG" ]; then
    rm "$WORK_FLAG"
    touch "$PAUSE_FLAG"
elif [ -f "$PAUSE_FLAG" ]; then
    rm "$PAUSE_FLAG"
    touch "$BREAK_FLAG"
elif [ -f "$BREAK_FLAG" ]; then
    rm "$BREAK_FLAG"
    touch "$WORK_FLAG"
else
    touch "$WORK_FLAG"
fi
