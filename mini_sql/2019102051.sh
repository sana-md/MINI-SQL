#!/bin/bash
for dir in "$@"
do
	python3 new.py "$dir"
done
