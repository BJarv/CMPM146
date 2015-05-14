from p6_game import Simulator


ANALYSIS = {}

def analyze(design):
    sim = Simulator(design)
    queue = []
    visited = []

    init = sim.get_initial_state()
    moves = sim.get_moves()
    next_state = sim.get_next_state(init, moves[0])
	
    position, abilities = next_state # or None if character dies
    i, j = position
    
    
    queue.append((init, [init]))
    visited.append(init)
	
    while queue:
        (prevstate, path) = queue.pop(0)
        for next in sim.get_moves():
             newstate = sim.get_next_state(prevstate, next)
             if (newstate is not None and newstate not in ANALYSIS):
                 if newstate not in visited:
                    ANALYSIS[newstate] = path
                    queue.append((newstate, path + [newstate]))
                    visited.append(newstate)
                 print newstate
             			 
	
    # TODO: fill in this function, populating the ANALYSIS dict
    raise NotImplementedError

def inspect((i,j), draw_line):
    # TODO: use ANALYSIS and (i,j) draw some lines
    found = False
    for next in ANALYSIS:
        print 'i ', i, 'nex:t ', next[0][0]
        if i is next[0][0] and j is next [0][1]:
           path = ANALYSIS[next]
           for n in range(len(path) - 1):
               found = True
               draw_line(path[n][0], path[n+1][0])
           draw_line(path[-1][0], (i,j))
           break
    if not found:
        print "Nothing was found"
    raise NotImplementedError