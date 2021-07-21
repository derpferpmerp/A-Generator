def distance(x1,y1,x2,y2,method=False):
	if not method: return None
	elif method == "diag":
		dx,dy = [abs(x1 - x2),abs(y1 - y2)]
	return abs(x1-x2) + abs(y1-y2)

print(ab_distance(0,3,4,0))