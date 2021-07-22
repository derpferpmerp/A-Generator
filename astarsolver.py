import numpy as np
import random
import sys
import math


# Coords
# Value = 0 (None)
# Value = 1 (Wall)
# Value = 2 (End Position)
# Value = 3 (Start Position)
if "-h" in sys.argv[1::]:
	sys.exit("-h: Help\n-d=NUM [Density Variable]\n-v [Verbose Mode]\n-w=NUM [Width of Grid]")
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

# CONFIG
w_val=6
verbose=False
density = 2
for sysarg in sys.argv[1::]:
	if "-m" in sysarg:
		maxv = int(sysarg.replace("-m=",""))
	if "-w" in sysarg:
		w_val = int(sysarg.replace("-w=",""))
	if "-v" in sysarg:
		verbose=True
	if "-d" in sysarg:
		density = float(sysarg.replace("-d=",""))

grd = gen_rand_grid(w_val, density=density)
#xs,ys = rPos(grd,0)
xs,ys = rPos(grd,0)
xe,ye = [0,0]
grd[xe,ye]=2
grd[xs,ys]=3
# END CONFIG

def recursive_perms(chrstart,chrend,arr,pcoords=False,initial=False,cllist=False):
	if initial:
		cl = rPos(arr,chrend,allcoords=True)
	else:
		cl = cllist
	for coord_list in cl:
		coordsdict = get_bounds(coord_list[0],coord_list[1],arr)
		movdict = {"l":[-1,0],"r":[1,0],"u":[0,-1],"d":[0,1]}
		outcoords = {"stage2":[]}
		outdct = {"stage1":[]}
		for pos_dir in list(coordsdict.keys()):
			if initial:
				outdct["stage1"].append(coord_list)
			for itr in [([coord_list[0] + movdict[pos_dir][0],coord_list[1] + movdict[pos_dir][1]])]:
				outcoords["stage2"] += list(get_bounds(itr[0],itr[1],arr,jcoords=True).values())
		outcoordsfinal = []
	try:
		outcoords["stage2"] = remove_dup(outcoords["stage2"])
	except UnboundLocalError:
		pass
	if not pcoords:
		pcoords = []
	for x1,y1 in outcoords["stage2"]:
		outcoordsfinal2 = []
		for gg in list(get_bounds(x1,y1,arr,jcoords=True).values()):
			if gg not in pcoords:
				outcoordsfinal2.append(gg)
		outcoordsfinal += outcoordsfinal2
	out = []
	for coorditer in remove_dup(outcoordsfinal):
		try:
			cval = arr[coorditer[0],coorditer[1]]
			if cval != 1:
				out.append([coorditer,arr[coorditer[0],coorditer[1]]])
		except IndexError:
			continue
	return out

crddone = []
vals = []
try:
	for crd,val in recursive_perms(3,2,grd,initial=True):
		crddone.append(crd)
		vals.append(val)
except UnboundLocalError:
	pass
dctstages = {}
for x in range(round(math.sqrt(w_val)+4)):
	if verbose:
		sys.stdout.write(f"Checking Generation {x}\r")
		sys.stdout.flush()
	done=False
	for crd2, val2 in recursive_perms(3,2,grd,initial=False,cllist=crddone):
		if val2 == 3:
			sys.exit(grd)
			done=True
		if crd2 not in crddone:
			crddone.append(crd2)
	if done:
		break

print("False")
