.PHONY: clean

.SUFFIXES:

CC = gcc
LDLIBS = -lm -lgsl -lgslcblas
#CFLAGS = -std=c99
CFLAGS = -Ofast
CCFLAGS =  #-g -Wall #-pg

OBJ3 =  make_graph.o tools.o

all: make_graph

make_graph : $(OBJ3)
	$(CC) $(OBJ3) -o $@ $(LDLIBS) $(CCFLAGS)

make_graph.o : make_graph.c
	$(CC) $(CFLAGS) -c $< -o $@ $(CCFLAGS)
tools.o : tools.c tools.h
	$(CC) $(CFLAGS) -c $< -o $@ $(CCFLAGS)

clean :
	rm $(OBJ3)
