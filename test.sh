#!/bin/bash
read -s -p "Enter Password for sudo: " sudoPW
echo $sudoPW | sudo -S echo "this is a new line" >> s.txt