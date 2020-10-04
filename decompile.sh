#!/bin/bash

if [[ -z "$1" ]]; then
	echo "usage: $(basename $0) <directory>"
	exit 1
fi

dir=$(realpath "$1")

for i in "$dir"/*; do
	if [[ -d "$i" ]]; then
		$0 "$i"
	else
		if [[ ${i: -4} != ".pyc" ]]; then
			continue
		fi

		output="${i%.*}".py
		echo "$i"
		uncompyle6 "$i" > "$output"
	fi
done
