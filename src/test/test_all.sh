#!/usr/bin/env bash

for file in /mnt/c/Users/Jonathan/Documents/code/icfp2019/part-1-initial/*.desc
do
  python3 /mnt/c/Users/Jonathan/Documents/code/icfp2019/src/test/test_strategy.py "$file" "$1" "$2"
done