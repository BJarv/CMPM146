from math import sqrt
from heapq import heappush, heappop

def find_path(source_point, destination_point, mesh):
	verbose = False
	boxes = mesh['boxes']
	adj = mesh['adj']
	search = biAStar
	path,visited = search(adj, source_point, destination_point)
	return path, visited

def pointToBox(point,graph):
	return_box = None
	for box in graph:
		if ((box[0] <= point[0]) and (box[1] >= point[0]) and (box[2] <= point[1]) and (box[3] >= point[1])):
			return_box = box
	return return_box

def bfs(graph, start_point,end_point):
    start = pointToBox(start_point,graph)
    end = pointToBox(end_point,graph)
    if (start is None) or (end is None): 
        print 'No path!'
        return [],[]
    boxPoint = {start: start_point}
    queue = [start]
    visited = []
    parent = {start: None}
    while queue:
        node = queue.pop(0)
        visited.append(node)
	for neighbor in graph[node]:
	  if neighbor not in visited:
	    queue.append(neighbor)
	    boxPoint[neighbor] = getBoxPoint(boxPoint[node], neighbor)
	    parent[neighbor] = node
	if node == end:
	  path, curr = [(boxPoint[node],end_point)], node
	  while parent[curr] is not None:
	    path.append((boxPoint[parent[curr]],boxPoint[curr]))
	    curr = parent[curr]
	  path.reverse()
	  return (path, visited)
    print 'No path!'
    return [],[]  
	  
def dij(graph, start_point,end_point):
    start = pointToBox(start_point,graph)
    end = pointToBox(end_point,graph)
    if (start is None) or (end is None): 
        print 'No path!'
        return [],[]
    boxPoint = {start: start_point}
    queue = [(0, start)]
    visited = []
    parent = {start: None}
    dist = { start:0 }
    while queue:
        nodeQ = heappop(queue)
        node = nodeQ[1]
        visited.append(node)
        if node == end:
	  path, curr = [(boxPoint[node],end_point)], node
	  while parent[curr] is not None:
	    path.append((boxPoint[parent[curr]],boxPoint[curr]))
	    curr = parent[curr]
	  path.reverse()
	  return (path, visited)
	for neighbor in graph[node]:
	  newPoint = getBoxPoint(boxPoint[node], neighbor)
          newDist = nodeQ[0] + distance(boxPoint[node], newPoint)
          if (neighbor not in dist) or (newDist < dist[neighbor]):
            boxPoint[neighbor] = newPoint
	    dist[neighbor] = newDist
	    heappush(queue, (newDist, neighbor))
	    parent[neighbor] = node
    print 'No path!'
    return [],[]  
    
def bidir(graph, start_point,end_point):
    start = pointToBox(start_point,graph)
    end = pointToBox(end_point,graph)
    if (start is None) or (end is None): 
        print 'No path!'
        return [],[]
    f_boxPoint, b_boxPoint = {start: start_point}, {end: end_point}
    queue = [(0, start, 'end' ),(0, end, 'start')]
    visited = []
    f_parent, b_parent = {start: None}, {end: None}
    f_dist, b_dist = { start:0 }, { end:0 }
    while queue:
        nodeQ = heappop(queue)
        prior, node, goal = nodeQ
        visited.append(node)
	if (node in b_parent) and (node in f_parent):
	  currF= currB = node
	  pathF, pathB = [], [(f_boxPoint[node],b_boxPoint[node])]
	  while f_parent[currF] is not None:
	    pathF.append((f_boxPoint[f_parent[currF]],f_boxPoint[currF]))
	    currF = f_parent[currF]
	  pathF.reverse()
	  while b_parent[currB] is not None:
	    pathB.append((b_boxPoint[b_parent[currB]],b_boxPoint[currB]))
	    currB = b_parent[currB]
	  print pathF + pathB
	  return pathF + pathB, visited
	for neighbor in graph[node]:
	  boxPoint = f_boxPoint if goal == 'end' else b_boxPoint
	  dist = f_dist if goal == 'end' else b_dist
	  parent = f_parent if goal == 'end' else b_parent
	  newPoint = getBoxPoint(boxPoint[node], neighbor)
          newDist = prior + distance(boxPoint[node], newPoint)
	  if (neighbor not in dist) or (newDist < dist[neighbor]):
            boxPoint[neighbor] = newPoint
	    dist[neighbor] = newDist
	    heappush(queue, (newDist, neighbor,goal))
	    parent[neighbor] = node
    print 'No path!'
    return [],[]  

def aStar(graph, start_point,end_point):
    start = pointToBox(start_point,graph)
    end = pointToBox(end_point,graph)
    if (start is None) or (end is None): 
        print 'No path!'
        return [],[]
    boxPoint = {start: start_point}
    queue = [(0, start)]
    visited = []
    parent = {start: None}
    dist = { start:0 }
    while queue:
        nodeQ = heappop(queue)
        node = nodeQ[1]
        visited.append(node)
        if node == end:
	  path, curr = [(boxPoint[node],end_point)], node
	  while parent[curr] is not None:
	    path.append((boxPoint[parent[curr]],boxPoint[curr]))
	    curr = parent[curr]
	  path.reverse()
	  return (path, visited)
	for neighbor in graph[node]:
	  newPoint = getBoxPoint(boxPoint[node], neighbor)
          newDist = dist[node] + distance(boxPoint[node], newPoint) 
          if (neighbor not in dist) or (newDist < dist[neighbor]):
	    heur = distance(newPoint,end_point)
            boxPoint[neighbor] = newPoint
	    dist[neighbor] = newDist
	    heappush(queue, (newDist+heur, neighbor))
	    parent[neighbor] = node
    print 'No path!'
    return [],[]  

def biAStar(graph, start_point,end_point):
    start = pointToBox(start_point,graph)
    end = pointToBox(end_point,graph)
    if (start is None) or (end is None): 
        print 'No path!'
        return [],[]
    f_boxPoint, b_boxPoint = {start: start_point}, {end: end_point}
    queue = [(0, start, 'end' ),(0, end, 'start')]
    visited = []
    f_parent, b_parent = {start: None}, {end: None}
    f_dist, b_dist = { start:0 }, { end:0 }
    while queue:
        nodeQ = heappop(queue)
        prior, node, goal = nodeQ
        visited.append(node)
	if (node in b_parent) and (node in f_parent):
	  currF= currB = node
	  pathF, pathB = [], [(f_boxPoint[node],b_boxPoint[node])]
	  while f_parent[currF] is not None:
	    pathF.append((f_boxPoint[f_parent[currF]],f_boxPoint[currF]))
	    currF = f_parent[currF]
	  pathF.reverse()
	  while b_parent[currB] is not None:
	    pathB.append((b_boxPoint[b_parent[currB]],b_boxPoint[currB]))
	    currB = b_parent[currB]
	  return pathF + pathB, visited
	for neighbor in graph[node]:
	  boxPoint = f_boxPoint if goal == 'end' else b_boxPoint
	  dist = f_dist if goal == 'end' else b_dist
	  parent = f_parent if goal == 'end' else b_parent
	  goal_point = end_point if goal == 'end' else start_point
	  newPoint = getBoxPoint(boxPoint[node], neighbor)
          newDist = dist[node] + distance(boxPoint[node], newPoint)
	  if (neighbor not in dist) or (newDist < dist[neighbor]):
	    heur = distance(newPoint,goal_point)
            boxPoint[neighbor] = newPoint
	    dist[neighbor] = newDist
	    heappush(queue, (newDist + heur, neighbor,goal))
	    parent[neighbor] = node
    print 'No path!'
    return [],[]  

    
def getBoxPoint(start_point, end_box):
  x,y = start_point 
  if start_point[0]<= end_box[0]: x = end_box[0]
  if start_point[0]>= end_box[1]: x = end_box[1]
  if start_point[1]<= end_box[2]: y = end_box[2]
  if start_point[1]>= end_box[3]: y = end_box[3] 
  return (x,y)

def distance(p1, p2):
  x1,y1 = p1
  x2,y2 = p2
  return sqrt((x2-x1)**2 + (y2-y1)**2)
		
