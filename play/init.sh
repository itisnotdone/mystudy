#!/bin/bash

# Install driver
sudo apt install python-pip
sudo apt install libncurses5-dev

sudo pip install --upgrade pip
sudo pip install selenium ptpython readchar

# Download server
# http://www.seleniumhq.org/download/

# Download geckodriver
# https://github.com/mozilla/geckodriver/releases

# Export the location of geckodriver
export PATH=$PATH:$PWD

# run selenium server
java -jar selenium-server-standalone-3.4.0.jar
# or
java -jar -Dwebdriver.server.session.timeout=86400 \
  -Dwebdriver.chrome.driver=$PWD/chromedriver \
  selenium-server-standalone-3.4.0.jar \
  -timeout 86400
