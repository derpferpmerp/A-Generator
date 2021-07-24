import numpy as np
from numpy.random import randint as rnd
import matplotlib.pyplot as plt
import subprocess
def maze(width=81, height=51, complexity=.75, density =.75, b=False, bl=False):
    # Only odd shapes
		if b:
			shape = ((height//2)*2, (width//2)*2)
		else:
			shape = ((height//2)*2, (width//2)*2)
    # Adjust complexity and density relative to maze size
		complexity = int(complexity*(5*(shape[0]+shape[1])))
		density    = int(density*(shape[0]//2*shape[1]//2))
		Z = np.zeros(shape, dtype=bool)
    # Fill borders
		if b:
			Z[0,:] = Z[-1,:] = 1
			Z[:,0] = Z[:,-1] = 1
    # Make isles
		for i in range(density):
				x, y = rnd(0,shape[1]//2)*2, rnd(0,shape[0]//2)*2
				Z[y,x] = 1
				for j in range(complexity):
						neighbours = []
						if x > 1:           neighbours.append( (y,x-2) )
						if x < shape[1]-2:  neighbours.append( (y,x+2) )
						if y > 1:           neighbours.append( (y-2,x) )
						if y < shape[0]-2:  neighbours.append( (y+2,x) )
						if len(neighbours):
								y_,x_ = neighbours[rnd(0,len(neighbours)-1)]
								if Z[y_,x_] == 0:
										Z[y_,x_] = 1
										Z[y_+(y-y_)//2, x_+(x-x_)//2] = 1
										x, y = x_, y_
		return [1 * Z if not bl else Z][0]

def gen_maze_img(w=15,h=15,c=0.75,d=0.75,brdr=True,m=0.5,bl2=True,grid=False):
	plt.figure(figsize=(w,h))
	if type(grid) == type(True):
		mzgenned = maze(width=w,height=h,complexity=c,density=d,b=brdr,bl=bl2)
	else:
		mzgenned = grid
	plt.imshow(mzgenned,cmap=plt.cm.binary,interpolation='nearest')
	plt.xticks([]),plt.yticks([])
	plt.savefig("lvl.png")
	return mzgenned * 1