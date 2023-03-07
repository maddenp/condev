LIB  = libworld.so
OBJS = $(SRCS:.c=.o)
SRCS = $(wildcard *.c)

.PHONY: all clean install

all: $(LIB)

clean:
	$(RM) $(LIB) $(OBJS)

install: $(LIB)
	cp -v $(LIB) $(PREFIX)/lib

$(LIB): $(OBJS)
	$(CC) $(CFLAGS) -shared -o $(LIB) $(OBJS)

%.o: %.c
	$(CC) $(CFLAGS) -c $<
