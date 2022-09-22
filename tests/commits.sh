#!/bin/bash

git rev-list --objects --all | awk '$2' | sort -k2 | uniq -cf1 | sort -rn |
    while read frequency sample file
    do 
       [ "blob" == "$(git cat-file -t $sample)" ] && echo -e "$frequency\t$file";
    done