#!/bin/bash

mkdir -p build &&\
cd "$_" && \
cmake .. && \
make && \
./Gravitational_Potential
