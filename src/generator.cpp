#include <iostream>

#include "sudoku.h"

using namespace std;

int main(int argc, char const *argv[])
{
    int it = 100;
    cerr << "Generating " << it << " puzzles..." << endl;
    for (int i = 0; i < it; ++i)
    {
        Sudoku s = Sudoku::random_sudoku();
        s.heuristic_small_start();
        cout << s << endl;
    }
    cerr << "Done !" << endl;

    return 0;
}