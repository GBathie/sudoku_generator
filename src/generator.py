import sys
from tqdm import tqdm
import numpy as np
import numpy.random as npr

def generate(it=10):
	s = np.zeros((9, 9), dtype=np.int)
	for i in range(9):
		for j in range(9):
			s[j,i] = (i + (6*(j%3)) - j//3 + 9) % 9 + 1
	
	# Swap random column / line in the same squares
	i1 = npr.randint(0, 3, it)
	i2 = npr.randint(0, 3, it)
	col = npr.randint(0, 2, it)
	for i in range(it):
		a = 3*i1[i] + i2[i]
		b = 3*i1[i] + (i2[i] + 1) % 3
		if col[i]:
			s[:,[a,b]] = s[:,[b,a]]
		else:
			s[[a,b],:] = s[[b,a],:]
	return s



DEFAULT_ITS = 10000
if __name__ == '__main__':
	try:
		assert len(sys.argv) >= 3
		n = int(sys.argv[1])
		fname = sys.argv[2]
		its = int(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_ITS
		with open(fname, "w+") as f:
			for _ in tqdm(range(n)):
				s = generate(its)
				f.write(''.join(str(x) for x in s.flatten()) + '\n')
	except:
		print(f'Usage: python3 {sys.argv[0]} <nb_sudokus> <output_file> [nb_iterations]')
		exit(1)