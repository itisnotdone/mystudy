#!/bin/zsh

WORK_DIR=`cat env.json | grep working_dir | awk '{print $2}' | tr -d '"' | tr -d ',''"'`
TEMP_DIR=`cat env.json | grep temporary_dir | awk '{print $2}' | tr -d '"' | tr -d ',''"'`

check_recording () {
  while inotifywait -r -q -e modify,move,create,delete $TEMP_DIR | read -r DIR OPS FILE; \
  do \
    clear; \
    echo "$DIR $OPS $FILE"; \
    ls -s --block-size=K $DIR; \
    date +%X; \
    sleep 1; \
  done
}

check_encoding () {
  while inotifywait -r -q -e modify,move,create,delete $WORK_DIR | read -r DIR OPS FILE; \
  do \
    clear; \
    echo "$DIR $OPS $FILE"; \
    ls -s --block-size=K $DIR; \
    date +%X; \
    sleep 1; \
  done
}

$1
