SRC := $(wildcard src/*.cpp)
OBJ := $(SRC:.cpp=.o)
CXXFLAGS := -Wall -Wextra -g -std=c++17 

all: main

main: $(OBJ)
	$(CXX) $(CXXFLAGS) -o $@ $^ 

pdf:
	cd latex &&	latexmk -pdf main.tex

clean:
	$(RM) $(OBJ)