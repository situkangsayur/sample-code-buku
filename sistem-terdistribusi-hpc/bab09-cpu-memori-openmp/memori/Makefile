CC ?= gcc
CXX ?= g++
all: bug raii
bug: bug.c
	$(CC) -g -fsanitize=address -fno-omit-frame-pointer $< -o $@
raii: raii.cpp
	$(CXX) -std=c++17 -O2 $< -o $@
clean:
	rm -f bug raii
