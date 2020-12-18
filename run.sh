#!/bin/bash
echo "start run.sh..."
echo "run TG_webAPI..."
nohup /usr/bin/python3 /workspace/TG_webAPI.py &
echo "run PublishMessage..."
nohup /usr/bin/python3 /workspace/PublishMessage.py &
echo "done run.sh"

