LIB  = libworld.a
OBJS = $(SRCS:.c=.o)
SRCS = $(wildcard *.c)

.PHONY: all clean install

all: $(OBJS)

clean:
	$(RM) $(LIB) $(OBJS)

install: $(LIB)
	cp -v $(LIB) $(PREFIX)/lib

$(LIB): $(OBJS)
	$(AR) -crs $(LIB) $(OBJS)

%.o: %.c
	$(CC) -c $<
