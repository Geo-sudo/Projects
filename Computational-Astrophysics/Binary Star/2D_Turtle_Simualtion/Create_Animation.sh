#!/bin/bash

convert -dispose previous -delay 2 -loop 0 ./frames/frame_*.eps "./animation.gif"
rm -rf frames
echo -e '\a'
echo -e '\007'
