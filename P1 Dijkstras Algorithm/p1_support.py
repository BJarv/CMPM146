
# Support code for P1
# https://courses.soe.ucsc.edu/courses/cmpm146/Spring15/01

def load_level(filename):
	
	#The following are dictionaries.
	#A dictionary is an unordered set of key-value pairs.
	#In these dicts, keys will be (i,j) pairs. Values will be the char.
	walls = {}
	spaces = {}
	waypoints = {}
	with open(filename, "r") as f:
		#Iterate through each line in file
		for j, line in enumerate(f.readlines()):
			#Iterate through each char in line
			for i, char in enumerate(line):
				#Skip if null plug
				if char == '\n':
					continue
				#If upper case...
				elif char.isupper():
					#... add to walls dict
					walls[(i,j)] = char
				#If it's not a wall it's a space.
				else:
					spaces[(i,j)] = char
					#If it's a lowercase letter it's also a waypoint.
					if char.islower():
						waypoints[char] = (i,j)


	#level itself is a dict with string keys and dict values.
	level = { 'walls': walls,
			  'spaces': spaces,
			  'waypoints': waypoints}

	return level


def show_level(level, path=[]):

	xs, ys = zip(*(level['spaces'].keys() + level['walls'].keys()))
	x_lo = min(xs)
	x_hi = max(xs)
	y_lo = min(ys)
	y_hi = max(ys)

	path_cells = set(path)

	chars = []

	for j in range(y_lo, y_hi+1):
		for i in range(x_lo, x_hi+1):

			cell = (i,j)
			if cell in path_cells:
				chars.append('*')
			elif cell in level['walls']:
				chars.append(level['walls'][cell])
			elif cell in level['spaces']:
				chars.append(level['spaces'][cell])
			else:
				chars.append(' ')
				
		chars.append('\n')

	print ''.join(chars)
