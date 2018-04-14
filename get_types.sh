#!/bin/bash

cat ${1} | tr " " "\n" | rev | cut -d / -f 1 | sort -u | sed '/^$/d' > ${2}
