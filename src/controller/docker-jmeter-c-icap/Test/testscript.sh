#!/bin/bash

DIR=${0%/*}'/input/'
ODIR=${0%/*}'/output/'
rm -rf ${ODIR} > /dev/null 2>&1
mkdir -p ${ODIR}

for file in "$DIR"*
do
    filename=${file##*/}
    /usr/bin/c-icap-client -i icap.sahith.in -p 443 -s gw_rebuild -f "$file" -o "$ODIR"/"$filename" -v
done
