CC ?= gcc
all: ilp branch rowcol false_sharing
ilp: ilp.c common.h
	$(CC) -O2 $< -o $@
branch: branch.c common.h
	$(CC) -O1 $< -o $@
rowcol: rowcol.c common.h
	$(CC) -O2 $< -o $@
false_sharing: false_sharing.c
	$(CC) -O2 -fopenmp $< -o $@
clean:
	rm -f ilp branch rowcol false_sharing
