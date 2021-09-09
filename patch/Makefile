CC = gcc  # C compiler
CFLAGS = -fPIC -Wall -Wextra -O2 -g  -lmkl_intel_ilp64 -lmkl_intel_thread -lmkl_core -liomp5 -lpthread -lm -ldl # C flags
LDFLAGS = -shared   # linking flags
RM = rm -f   # rm command
TARGET_LIB = fftw_intelmkl_wrapper.so  # target lib

SRCS = fftw_wrapper.c  # source files
OBJS = $(SRCS:.c=.o)

.PHONY: all
all: ${TARGET_LIB}

$(TARGET_LIB): $(OBJS)
	$(CC) ${LDFLAGS} -o $@ $^

$(SRCS:.c=.d):%.d:%.c
	$(CC) $(CFLAGS) -MM $< >$@

include $(SRCS:.c=.d)

.PHONY: clean
clean:
	-${RM} ${TARGET_LIB} ${OBJS} $(SRCS:.c=.d)
