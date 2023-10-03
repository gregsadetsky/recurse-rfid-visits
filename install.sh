#!/usr/bin/env bash
if [ "$EUID" -ne 0 ]
  then echo "Please run this script with sudo"
  exit 1
fi
echo "Write here your API access token: (entry to skip)"
read TOKEN
if [ -z "$TOKEN" ]
then
    echo "API access token is empty, skipping"
else
    echo API_TOKEN=$TOKEN > /root/.env
fi

cd octoberry
pip install -e .
sudo apt update && sudo apt install -y mpv

cd ../service
sudo ./install-service.sh