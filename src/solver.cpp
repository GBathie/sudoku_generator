#include <iostream>

#include "sudoku.h"

using namespace std;

int main(int argc, char const *argv[])
{
    for (int i = 0; i < 10; ++i)
    {
        Sudoku s = Sudoku::random_sudoku();
        s.heuristic_small_start();
        cout << s << endl;
    }

    return 0;
}