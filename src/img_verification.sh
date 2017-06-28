#!/bin/sh

isPicture=$(file -b -i $1 | grep image | wc -l);

if [ $isPicture -ne 1 ]
then
    echo "INVALID FORMAT";
    rm -f $1
else
    echo "OK"
fi