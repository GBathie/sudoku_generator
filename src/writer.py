import sys
from tqdm import tqdm

def hardness(h):
	return (('\\ding{72}') * h) + (('\\ding{73}') * (5 - h))

sol_scale = .5
main_scale = 1
def write_header(f, sol, h):
	scale = sol_scale if sol else main_scale
	f.write(
f'''%
\\begin{{figure}}[{'H' if sol else 'htbp'}]
\\centering
\\stepcounter{{sudokucounter}}
\\caption*{{\\textbf{{Sudoku \\arabic{{sudokucounter}}}} ({hardness(h)}) }}
\\begin{{tikzpicture}}[scale={scale}, every node/.style={{scale={scale}}}]
    \\draw (0, 0) grid (9, 9);
    \\draw[very thick, scale=3] (0, 0) grid (3, 3);
''')

def write_footer(f, sol):
	f.write(f'''%
\\end{{tikzpicture}}
\\end{{figure}}
''')



def compute_hardness(data):
	nnz = sum(1 for c in data if c != '0')
	if nnz < 18:
		return 5
	if nnz < 20:
		return 4
	if nnz < 24:
		return 3
	if nnz < 30:
		return 2
	if nnz < 36:
		return 1
	return 0

def print_sudoku(data, ofile, h):
	assert len(data) == 81, 'Bad sudoku length : ' + str(data)
	write_header(ofile, False, h)
	for i in range(81):
		c = data[i]
		if c != '0':
			x = i % 9
			y = i // 9
			ofile.write(f'\\node[anchor=center] at ({x+.5}, {8.5-y}) {{{c}}};\n')
	write_footer(ofile, False)

def print_solution(data, ofile, h, sol):
	assert len(data) == 81, 'Bad sudoku length : ' + str(data)
	assert len(sol) == 81,  'Bad solution length : ' + str(sol)
	write_header(ofile, True, h)
	for i in range(81):
		c = data[i]
		x = i % 9
		y = i // 9
		if c == '0':
			ofile.write(f'\\node[anchor=center] at ({x+.5}, {8.5-y}) {{{sol[i]}}};\n')
		else:
			ofile.write(f'\\node[anchor=center] at ({x+.5}, {8.5-y}) {{\\textbf{{{c}}}}};\n')
	write_footer(ofile, True)

def parse_sudoku(i, l, odirname, main_ofile_sud, main_ofile_sol):
	sud, sol = l.strip().split(' ')
	h = compute_hardness(sud)
	sudfname = f'sudoku{i.zfill(3)}.sud.tex'
	solfname = f'sudoku{i.zfill(3)}.sol.tex'
	with open(odirname + '/' + sudfname, "w+") as f:
		print_sudoku(sud, f, h)
	with open(odirname + '/' + solfname, "w+") as f:
		print_solution(sud, f, h, sol)
	main_ofile_sol.write(f'\\input{{{solfname}}}%\n')
	main_ofile_sud.write(f'\\input{{{sudfname}}}%\n')
		

def parse_file(fname, odirname):
	i = 0
	with open(fname, 'r+') as f:
		with open(odirname + '/all_sud.tex', 'w+') as main_ofile_sud:
			with open(odirname + '/all_sol.tex', 'w+') as main_ofile_sol:
				for l in tqdm(f.readlines()):
					parse_sudoku(str(i), l, odirname, main_ofile_sud, main_ofile_sol)
					i += 1

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print(f'Usage: python3 {sys.argv[0]} <sudokus_data_file> <output_dir>')
		exit(1)

	parse_file(sys.argv[1], sys.argv[2])