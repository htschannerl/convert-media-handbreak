#!/bin/bash
export LIBVA_DRIVER_NAME=iHD
CMD="/usr/bin/HandBrakeCLI -Z \"$1\" -i \"$2\" -o \"$3\"" 
eval "$CMD"
echo $CMD
echo $1
echo $2
echo $3
