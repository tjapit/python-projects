CC = gcc
CFLAGS = -Wall -std=c99 -g

all: clean ping

ping: 
	$(CC) $(CFLAGS) ping.c -o ping

clean:
	rm -f *.o
	rm -f ping
	rm -f *.exe
	rm -f *.exe.stackdump
