#!/bin/bash

WORK_DIR=`cat env.json | grep working_dir | awk '{print $2}' | tr -d '"' | tr -d ',''"'`
TEMP_DIR=`cat env.json | grep temporary_dir | awk '{print $2}' | tr -d '"' | tr -d ',''"'`

function start_server {
  java \
    -jar \
    -Dwebdriver.server.session.timeout=86400 \
    -Dwebdriver.chrome.driver=$PWD/chromedriver selenium-server-standalone-3.4.0.jar \
    -timeout 86400
}

function check_odd {
  while true; \
  do \
    SS=`ls -tl $TEMP_DIR | egrep '^d.*rMD-session.*done-1$' | awk '{print $9}' | tail -1`; \
    if [[ ! -z $SS ]]; then \
      recordmydesktop --rescue $TEMP_DIR/$SS; \
      rm -rv $TEMP_DIR/$SS; \
    else echo `date`' nothing to encode for done-1'; \
    fi; \
    sleep 6; \
  done
}

function check_even {
  while true; \
  do \
    SS=`ls -tl $TEMP_DIR | egrep '^d.*rMD-session.*done-2$' | awk '{print $9}' | tail -1`; \
    if [[ ! -z $SS ]]; then \
      recordmydesktop --rescue $TEMP_DIR/$SS; \
      rm -rv $TEMP_DIR/$SS; \
    else echo `date`' nothing to encode for done-2'; \
    fi; \
    sleep 6; \
  done
}

function check_encoding_proc {
  while true; \
  do \
    clear; \
    top -w 512 -cbn 1 -U dongwon | egrep 'COMMAND|rMD-session' | egrep -v 'grep'; \
    sleep 2; \
  done
}

function check_temp_dirs {
  watch "ls -t $TEMP_DIR | grep rMD"
}

function check_recording_proc {
  while true; do clear; ps -u | egrep 'recordmydesktop' | awk -F 'recordmydesktop' '{print $2}' | egrep '\.ogv' | sort; sleep 2; done
}

function playing() {
  sleep 2
  DISPLAY=:0 python play.py
}

$1
