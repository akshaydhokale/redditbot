#!/bin/sh

source_root="$1"
NOW=$(date +"%F-%H-%M-%S")

python3 $source_root/src/stock_symbol_bot.py > $source_root/logs/log-$NOW
