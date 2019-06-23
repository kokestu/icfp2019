#!/usr/bin/env bash

for file in /mnt/c/Users/Jonathan/Documents/code/icfp2019/part-1-initial/*
do
  python3 "$1" "$file"
done