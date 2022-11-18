#!/bin/bash
DISPLAY=:1 your_qt_application
ffmpeg -f x11grab -s 1024x768 -i :1 -r 30 -preset ultrafast output.mp4
