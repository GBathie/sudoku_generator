#pragma once

#include <vector>
#include <array>
#include <iostream>
#include <string>
#include <fstream>

constexpr int BOARD_SIZE = 9;

typedef std::vector<bool> Vb;
typedef std::vector<Vb> VVb;
typedef std::array<int, BOARD_SIZE> Ai;
typedef std::vector<int> Vi;
typedef std::vector<Vi> VVi;

template <class T>
using Grid = std::array<std::array<T, BOARD_SIZE>, BOARD_SIZE>;

class Sudoku
{
public:
    Sudoku(const std::string &s);

    void debug();

    int64_t count_solutions(int i = 0, int j = 0);
    int unique_solution(int i = 0, int j = 0);
    void solve();

    std::string find_minimal_start();
    std::string position() const;

    void heuristic_small_start();
    // bool unique_solution(); // TODO

    static Sudoku random_sudoku();

    friend std::ostream &operator<<(std::ostream &os, const Sudoku &s);
private:
    Grid<int> board;
    /* legal[i][j][k] indicates "how many times" k is legal in cell i,j. 
     * It should be <= 1, You can play k iff it is 1.
     * It is used to efficiently compute legal moves with play/unplay: 
     * when adding the k number in some cell, decrease legal[:][:][k] on its line and column,
     * and conversely when removing the number from the cell.
     */
    Grid<Ai> legal; 
    std::string initial_pos;

    bool solve(int i, int j);
    void play(int i, int j, int k);
    void unplay(int i, int j);

    void find_minimal_start(int i, int j, int w, int &best_w, std::string &best);

};