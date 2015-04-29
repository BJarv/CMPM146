from p1_support import load_level, show_level
from math import sqrt
from heapq import heappush, heappop


def dijkstras_shortest_path(src, dst, graph, adj):
    #dictionaries
    prev = {}
    dist = {}

    #initial values for dictionaries
    dist[src] = 0
    prev[src] = None
    
    #heapq of unvisited nodes
    q = []

    #push initial value
    heappush(q, (0, src))

    #while we have values in the immediate surrounding unvisited nodes we plan to visit, loop
    while q:
    	#pull a node out of q and get pertinent information about node within and surrounding nodes
    	u = heappop(q)
    	_, cell = u
    	neighbors = adj(graph, cell)

    	#check neighbors and inserting info from shortest path
    	for n in neighbors:
    		alt = dist[cell] + distance(cell, n)
    		if n not in dist or alt < dist[n]:
    			dist[n] = alt
    			prev[n] = cell
    			heappush(q, (alt, n))
    			#if found destination, return path immediately
    			if n == dst: 
    				return traceback(prev, n, src)

def traceback(cells, cell, source): #find path of all
	path = []
	while cell != None:
		path.append(cell)
		cell = cells[cell]
	return path

def navigation_edges(level, cell): #find all edges around node
    steps = []
    x, y = cell
    for dx in [-1,0,1]:
	    for dy in [-1,0,1]:
	        next_cell = (x + dx, y + dy)
	        dist = sqrt(dx*dx+dy*dy)
	        if dist > 0 and next_cell in level['spaces']:
	            steps.append(next_cell)
    return steps

def distance(cell1, cell2): #calculate distance from one node to the next
	x1, y1 = cell1
	x2, y2 = cell2
	return sqrt((x2-x1)**2 + (y2-y1)**2)

def test_route(filename, src_waypoint, dst_waypoint):
	#Level gets stored
	level = load_level(filename)

	#Level gets drawn on screen
	show_level(level)
	
	#src and dst are set.
	src = level['waypoints'][src_waypoint]
	dst = level['waypoints'][dst_waypoint]

	#Path is found.
	path = dijkstras_shortest_path(src, dst, level, navigation_edges)

	if path:
		show_level(level, path)
	else:
		print "No path possible!"

if __name__ ==  '__main__':
	import sys
	#Store the relevant arguments on the cmd line
	_, filename, src_waypoint, dst_waypoint = sys.argv
	test_route(filename, src_waypoint, dst_waypoint)
