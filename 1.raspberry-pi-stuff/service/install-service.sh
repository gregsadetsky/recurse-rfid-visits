#!/usr/bin/bash

echo "Moving ocptopus.service to /etc/systemd/system"
mv ocptopus.service /etc/systemd/system
systemctl daemon-reload
if [ $? -ne 0 ]; then
  exit 1
fi

echo "Enabling ocptopus.service"
systemctl enable ocptopus
if [ $? -ne 0 ]; then
  exit 1
fi

echo "Starting ocptopus.service"
systemctl start ocptopus
if [ $? -ne 0 ]; then
  exit 1
fi

exit 0