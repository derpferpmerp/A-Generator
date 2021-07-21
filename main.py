import numpy as np
import random


def gen_rand_grid(d, density=1):
	try:
		grid = np.zeros((d, d), int)
		choices = np.random.choice(grid.size,random.randrange(round((3 / 4) * d * density), d * density), replace=False)
		grid.ravel()[choices] = 1
		return grid
	except ValueError:
		return None

def get_bounds(x1,y1,arr):
	dctout = {}
	for direction,cl in [["l",[-1,0]],["r",[1,0]],["u",[0,-1]],["d",[0,1]]]:
		for coord in [x1 + cl[0],y1 + cl[1]]:
			#print(f"{direction}: {coord}")
			if coord < 0:
				cont = False
				break
			cont = True

		if not cont: continue
		dctout[direction] = arr[y1 + cl[0],x1 + cl[1]]
		#print([y1 + cl[0],x1 + cl[1]])
	return dctout

grd = gen_rand_grid(6, density=2)
print(grd)
print(get_bounds(0,0,grd))