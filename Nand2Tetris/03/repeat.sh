#!/bin/bash

for i in {0..7}; do
#    echo "Bit(in=in[$i], load=load, out=out[$i]);" >> Register.hdl
#    echo "Register(in=in, load=, out=register$i);" >> RAM8.hdl
    echo "RAM8(in=in, load=load$i, address=address[0..2], out=ram$i);" >> RAM64.hdl
done