#!/bin/csh -f

unsetenv DISPLAY

nohup matlab < $1 > $2 &

