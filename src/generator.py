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



if __name__ == '__main__':
	s = generate(10000)
	print(s)
	print(list(s.flatten()))