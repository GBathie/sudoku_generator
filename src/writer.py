import sys
from tqdm import tqdm

def hardness(h):
	return (('\\ding{72}') * h) + (('\\ding{73}') * (5 - h))

sol_scale = .5
main_scale = 1
def write_header(f, sol, h):
	scale = sol_scale if sol else main_scale
	f.write(f'''\\begin{{figure}}[htbp]
\\centering
\\stepcounter{{sudokucounter}}
\\caption*{{\\textbf{{Sudoku \\arabic{{sudokucounter}}}} ({hardness(h)}) }}
\\begin{{tikzpicture}}[scale={scale}, every node/.style={{scale={scale}}}]
    \\draw (0, 0) grid (9, 9);
    \\draw[very thick, scale=3] (0, 0) grid (3, 3);\n''')

def write_footer(f):
	f.write('''
\\end{tikzpicture}
\\end{figure}
''')


def print_sudoku(l, odirname, main_ofile_sud, main_ofile_sol):
	i, t, h, data = l.strip().split(' ')
	assert len(data) == 81, 'Bad sudoku length'
	h = int(h)
	sol = t == 's'
	fname = f'sudoku{i.zfill(3)}.' + ('sol.tex' if sol else 'sud.tex')
	with open(odirname + '/' + fname, "w+") as ofile:
		write_header(ofile, sol, h)
		for i in range(81):
			c = data[i]
			if c != '0':
				x = i % 9
				y = i // 9
				ofile.write(f'\\node[anchor=center] at ({x+.5}, {8.5-y}) {{{c}}};\n')
		write_footer(ofile)
		if sol:
			main_ofile_sol.write(f'\\input{{{fname}}}\n')
		else:
			main_ofile_sud.write(f'\\input{{{fname}}}\n')

def parse_file(fname, odirname):
	with open(fname, 'r+') as f:
		with open(odirname + '/all_sud.tex', 'w+') as main_ofile_sud:
			with open(odirname + '/all_sol.tex', 'w+') as main_ofile_sol:
				for l in tqdm(f.readlines()):
					print_sudoku(l, odirname, main_ofile_sud, main_ofile_sol)


if __name__ == '__main__':
	if len(sys.argv) != 3:
		print(f'Usage: python3 {sys.argv[0]} <sudokus_data_file> <output_dir>')
		exit(0)

	parse_file(sys.argv[1], sys.argv[2])