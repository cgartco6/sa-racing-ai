#!/bin/bash
sudo apt update && sudo apt install -y python3.11 python3.11-venv python3-pip postgresql postgresql-contrib
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "Ubuntu setup complete"
