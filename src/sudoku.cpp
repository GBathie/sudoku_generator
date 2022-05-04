#include "sudoku.h"

#include <cassert>
#include <sstream>
#include <random>
#include <algorithm>

using namespace std;

Sudoku::Sudoku(const std::string &s) : board(), legal(), initial_pos(s)
{
    assert(initial_pos.size() == 81);
    for (int i = 0; i < BOARD_SIZE; ++i)
        for (int j = 0; j < BOARD_SIZE; ++j)
            for (int k = 0; k < BOARD_SIZE; ++k)
                legal[i][j][k] = 1;

    for (int i = 0; i < BOARD_SIZE; ++i)
        for (int j = 0; j < BOARD_SIZE; ++j)
            if (initial_pos[i*BOARD_SIZE + j] != '0')
                play(i, j, initial_pos[i*BOARD_SIZE + j] - '0');
            else
                board[i][j] = 0;
}

void Sudoku::debug()
{
    for (int i = 0; i < BOARD_SIZE; ++i)
    {
        if (i%3 == 0)
            cerr << "  -----  -----  -----  " << endl;
        for (int j = 0; j < BOARD_SIZE; ++j)
        {
            if (j%3 == 0)
                cerr << "||";
            else
                cerr << "|";

            if (board[i][j] == 0)
                cerr << " ";
            else
                cerr << board[i][j];

        }
        cerr << "||" << endl;

    }
    cerr << "  -----  -----  -----  " << endl;
}


int64_t Sudoku::count_solutions(int i, int j)
{
    if (i == BOARD_SIZE)
        i = 0, ++j;

    if (j == BOARD_SIZE)
        return 1;

    if (board[i][j] != 0)
        return count_solutions(i+1, j);

    int64_t res = 0;

    for (int k = 0; k < BOARD_SIZE; ++k)
    {
        if (legal[i][j][k] == 1)
        {
            play(i, j, k+1);
            res += count_solutions(i+1, j);
            unplay(i, j);
        }
    }

    return res;
}



void Sudoku::play(int i, int j, int k)
{
    board[i][j] = k;
    --k;
    for (int l = 0; l < BOARD_SIZE; ++l)
    {
        --legal[i][l][k];
        --legal[l][j][k];
    }
    int si = 3*(i / 3), sj = 3*(j / 3);
    for (int l = 0; l < 3; ++l)
        for (int m = 0; m < 3; ++m)
            --legal[si + l][sj + m][k];
}

void Sudoku::unplay(int i, int j)
{
    int k = board[i][j] - 1;
    board[i][j] = 0;
    for (int l = 0; l < BOARD_SIZE; ++l)
    {
        ++legal[i][l][k];
        ++legal[l][j][k];
    }
    int si = 3*(i / 3), sj = 3*(j / 3);
    for (int l = 0; l < 3; ++l)
        for (int m = 0; m < 3; ++m)
            ++legal[si + l][sj + m][k];
}


void Sudoku::solve()
{
    solve(0, 0);
}

bool Sudoku::solve(int i, int j)
{

    if (i == BOARD_SIZE)
        i = 0, ++j;

    if (j == BOARD_SIZE)
        return true;

    if (board[i][j] != 0)
        return solve(i+1, j);

    bool res;

    for (int k = 0; k < BOARD_SIZE; ++k)
    {
        if (legal[i][j][k] == 1)
        {
            play(i, j, k+1);
            res = solve(i+1, j);
            if (res)
                return true;
            unplay(i, j);
        }
    }

    return false;
}



string Sudoku::find_minimal_start()
{
    string res = position();
    int w = 81;
    find_minimal_start(0, 0, 81, w, res);
    return res;
}

void Sudoku::find_minimal_start(int i, int j, int w, int &best_w, string &best)
{

    if (i == BOARD_SIZE)
        i = 0, ++j;

    if (j == BOARD_SIZE)
        return;

    if (w < best_w)
    {
        best_w = w;
        best = position();
    }

    if (count_solutions() != 1)
        return;

    int k = board[i][j];    
    unplay(i, j);
    find_minimal_start(i+1, j, w-1, best_w, best);
    play(i, j, k);

}

string Sudoku::position() const
{
    stringstream ss;
    for (int i = 0; i < BOARD_SIZE; ++i)
        for (int j = 0; j < BOARD_SIZE; ++j)
            ss << board[i][j];

    return ss.str();
}


void Sudoku::heuristic_small_start()
{
    static random_device rd;
    static default_random_engine rng(rd());

    vector<pair<int,int>> coords;
    for (int i = 0; i < BOARD_SIZE; ++i)
        for (int j = 0; j < BOARD_SIZE; ++j)
            coords.emplace_back(i, j);

    shuffle(coords.begin(), coords.end(), rng);
    
    int k;
    for (auto &[x,y] : coords)
    {
        k = board[x][y];

        assert(k != 0);
        unplay(x, y);
        if (unique_solution() != 1)
            play(x, y, k);
    }
}

// Returns 1 iff there is a unique solution, otherwise anything > 1 or 0
int Sudoku::unique_solution(int i, int j)
{
    if (i == BOARD_SIZE)
        i = 0, ++j;

    if (j == BOARD_SIZE)
        return 1;

    if (board[i][j] != 0)
        return unique_solution(i+1, j);

    int count = 0;
    for (int k = 0; k < BOARD_SIZE; ++k)
    {
        if (legal[i][j][k] == 1)
        {
            play(i, j, k+1);
            count += unique_solution(i+1, j);
            unplay(i, j);

            if (count > 1)
                return count;
        }
    }
    return count;
}


std::ostream &operator<<(std::ostream &os, const Sudoku &s)
{
    os << s.position() << " " << s.initial_pos;
    return os;
}


Grid<int> default_grid {{
    {{1,2,3, 4,5,6, 7,8,9}},
    {{4,5,6, 7,8,9, 1,2,3}},
    {{7,8,9, 1,2,3, 4,5,6}},

    {{2,3,1, 5,6,4, 8,9,7}},
    {{5,6,4, 8,9,7, 2,3,1}},
    {{8,9,7, 2,3,1, 5,6,4}},

    {{3,1,2, 6,4,5, 9,7,8}},
    {{6,4,5, 9,7,8, 3,1,2}},
    {{9,7,8, 3,1,2, 6,4,5}}
    }};

Sudoku Sudoku::random_sudoku()
{
    static random_device rd;
    static default_random_engine rng(rd());

    Grid<int> g = {};

    Vi nb_perm = {1,2,3,4,5,6,7,8,9};
    shuffle(nb_perm.begin(), nb_perm.end(), rng);
    Vi row_perm = {0,1,2,3,4,5,6,7,8};
    Vi col_perm = {0,1,2,3,4,5,6,7,8};
    // Permute columns and rows only within the same 3x3 block
    for (int i = 0; i < BOARD_SIZE; i += 3)
    {
        shuffle(row_perm.begin() + i, row_perm.begin() + i + 3, rng);
        shuffle(col_perm.begin() + i, col_perm.begin() + i + 3, rng);
    }

    for (int i = 0; i < BOARD_SIZE; ++i)
        for (int j = 0; j < BOARD_SIZE; ++j)
            g[i][j] = nb_perm[default_grid[row_perm[i]][col_perm[j]] - 1];


    string pos = "";
    for (int i = 0; i < BOARD_SIZE; ++i)
        for (int j = 0; j < BOARD_SIZE; ++j)
            pos += '0' + g[i][j];

    return Sudoku(pos);
}
