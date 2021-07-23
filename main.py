import math
import random
import re
import sys
import numpy as np
from tools import maze as genrd

# Coords
# Value = 0 (None)
# Value = 1 (Wall)
# Value = 2 (End Position)
# Value = 3 (Start Position)
if "-h" in sys.argv[1::]:
	sys.exit("-h: Help\n-d=NUM [Density Variable]\n-v [Verbose Mode]\n-w=NUM [Width of Grid]\n-r [Switch to Random Maze Generation]\n-c=NUM [Complexity Variable]")
def gen_rand_grid(d, density=1, opt="NICE", cmp=0.75):
	if opt == "RANDOM":
		try:
			grid = np.zeros((d, d), int)
			choices = np.random.choice(grid.size,random.randrange(round((3 / 4) * d * density), d * density), replace=False)
			grid.ravel()[choices] = 1
			return grid
		except ValueError:
			return None
	else:
		return genrd(width=d,height=d,density=round(3/4 * d) * density,complexity=cmp)

def distance(x1,y1,x2,y2):
	return round(math.sqrt(abs(x2-x1)**2 + abs(y2-y1)**2))
	

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

def gen_ending_coords(arr,sx,sy,seek=0):
	dcoords, ddist = [[],[]]
	for x,y in [list(g) for g in list(zip(*np.nonzero(arr == seek)))]:
		dcoords.append([x,y])
		ddist.append(distance(x,y,sx,sy))
	maxval = dcoords[ddist.index(max(ddist))]
	return maxval
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
rndm="NICE"
comp = 0.75
for sysarg in sys.argv[1::]:
	if "-m" in sysarg:
		maxv = int(sysarg.replace("-m=",""))
	if "-w" in sysarg:
		w_val = int(sysarg.replace("-w=",""))
	if "-v" in sysarg:
		verbose=True
	if "-d" in sysarg:
		density = float(sysarg.replace("-d=",""))
	if "-r" in sysarg:
		rndm = "RANDOM"
	if "-c" in sysarg:
		comp = float(sysarg.replace("-c=",""))
		if comp > 1 or comp < 0:
			comp = 0.75

grd = gen_rand_grid(w_val, density=density, opt=rndm, cmp=comp)
#xs,ys = rPos(grd,0)
xs,ys = [1,1]
xe,ye = gen_ending_coords(grd,xs,ys)
grd[xe,ye]=2
grd[xs,ys]=3
# END CONFIG
if "-N" in sys.argv[1::]:
	sys.exit(grd)
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

def rec_pattern(arr,char=0,mn=3):
	flist = []
	for h_iter in range(round(math.sqrt(arr.size))):
		hlist = []
		for w_iter in range(round(math.sqrt(arr.size))):
			hlist.append(arr[h_iter,w_iter])
		flist.append(hlist)
	vertout = []
	for vert in range(len(flist)):
		vertout.append(list(list(zip(*flist))[vert]))
	horizontalcombd = [gg for gg in ["".join(str(g) for g in x) for x in flist]]
	vertcombd = [gg for gg in ["".join(str(g) for g in x) for x in vertout]]
	ol = {"Values":[]}
	for itr in range(len(horizontalcombd)):
		try:
			horizontalperms = re.search("".join([str(char) for x in range(mn)]), str(horizontalcombd[itr])).span()
			ol["Values"].append([[itr,horizontalperms[0]],[itr,horizontalperms[1]]])
		except AttributeError:
			pass
	for itr in range(len(vertcombd)):
		try:
			vertperms = re.search("".join([str(char) for x in range(mn)]), str(vertcombd[itr])).span()
			ol["Values"].append([[itr,vertperms[0]],[itr,vertperms[1]]])
		except AttributeError:
			pass
	fout = []
	for fv in ol["Values"]:
		diffx, diffy = [abs(fv[0][0] - fv[1][0]), abs(fv[0][1] - fv[1][1])]
		if diffy > 0:
			fout.append([[fv[0][0],x] for x in range(fv[0][1],fv[1][1])])
		elif diffx > 0:
			fout.append([[x,fv[0][1]] for x in range(fv[0][0],fv[1][0])])
	return fout



crddone = []
vals = []
try:
	for crd,val in recursive_perms(3,2,grd,initial=True):
		crddone.append(crd)
		vals.append(val)
except UnboundLocalError:
	pass
dctstages = {}
for x in range(round(w_val*4)):
	if verbose:
		sys.stdout.write(f"Checking Generation {x}\r")
		sys.stdout.flush()
	done=False
	for crd2, val2 in recursive_perms(3,2,grd,initial=False,cllist=crddone):
		if val2 == 3:
			strout = rec_pattern(grd)
			print(grd)
			sys.exit(str(strout))
			#done=True
		if crd2 not in crddone:
			crddone.append(crd2)
	if done:
		break

print("False")
