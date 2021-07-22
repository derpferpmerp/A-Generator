import numpy as np
import random


# Coords
# Value = 0 (None)
# Value = 1 (Wall)
# Value = 2 (End Position)
# Value = 3 (Start Position)

def gen_rand_grid(d, density=1):
	try:
		grid = np.zeros((d, d), int)
		choices = np.random.choice(grid.size,random.randrange(round((3 / 4) * d * density), d * density), replace=False)
		grid.ravel()[choices] = 1
		return grid
	except ValueError:
		return None

def get_bounds(x1,y1,arr,jcoords=False):
	dctout = {}
	for direction,cl in [["l",[-1,0]],["r",[1,0]],["u",[0,-1]],["d",[0,1]]]:
		for coord in [x1 + cl[0],y1 + cl[1]]:
			if coord < 0:
				cont = False
				break
			cont = True

		if not cont: continue
		try:
			if jcoords:
				dctout[direction] = [y1 + cl[0],x1 + cl[1]]
			else:
				dctout[direction] = arr[y1 + cl[0],x1 + cl[1]]
		except IndexError:
			continue
	return dctout

def rPos(arr,seek,allcoords=False):
	validstarting = np.nonzero(grd == seek)
	coords = list(zip(*validstarting))
	if allcoords:
		return [list(x) for x in coords]
	return list(coords[random.randrange(0,len(coords)-1)])

def remove_dup(original_list):
	lst2 = []
	for x in original_list:
		if x not in lst2:
			lst2.append(x)
	return lst2

grd = gen_rand_grid(6, density=2)
xs,ys = rPos(grd,0)
xe,ye = rPos(grd,0)
grd[xe,ye]=2
grd[xs,ys]=3

def recursive_perms(chrstart,chrend,arr,pcoords=False):
	for coord_list in rPos(arr,chrend,allcoords=True):
		coordsdict = get_bounds(coord_list[0],coord_list[1],arr)
		movdict = {"l":[-1,0],"r":[1,0],"u":[0,-1],"d":[0,1]}
		newcoords = []
		coord2get = [list(x) for x in list(zip(*np.nonzero(arr == chrstart)))][0]
		outcoords = {"stage2":[]}
		for pos_dir in list(coordsdict.keys()):
			newcoords.append([coord_list[0] + movdict[pos_dir][0],coord_list[1] + movdict[pos_dir][1]])
			for itr in [([coord_list[0] + movdict[pos_dir][0],coord_list[1] + movdict[pos_dir][1]])]:
				outcoords["stage2"] += list(get_bounds(itr[0],itr[1],arr,jcoords=True).values())
		outcoordsfinal = []
	outcoords["stage2"] = remove_dup(outcoords["stage2"])
	if not pcoords:
		pcoords = []
	for x1,y1 in outcoords["stage2"]:
		if pcoords:
			if [x1,y1] not in pcoords:
				outcoordsfinal += (list(get_bounds(x1,y1,arr,jcoords=True).values()))
		else:
			outcoordsfinal += (list(get_bounds(x1,y1,arr,jcoords=True).values()))
	return remove_dup(outcoordsfinal)

print(recursive_perms(3,2,grd))
print(grd)