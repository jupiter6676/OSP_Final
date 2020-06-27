#!/bin/bash


echo "create directory..."
sudo mkdir -p /usr/local/bin/setup
sudo mkdir -p /usr/local/bin/setup/templates

echo "copy files to temp directory..."
sudo cp app.py /usr/local/bin/setup
#sudo cp page.html /usr/local/bin/setup/templates	# 둘 중 어느거?
sudo cp home.html /usr/local/bin/setup/templates

cd /usr/local/bin/setup


sudo chmod -R 755 /usr/local/bin/setup/
flask run
