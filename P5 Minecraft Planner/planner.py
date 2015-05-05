import json
with open('Crafting.json') as f:
	Crafting = json.load(f)

print Crafting['Items']
print Crafting['Initial']
print Crafting['Goal']
print Crafting['Recipes']['craft stone_pickaxe at bench']


def make_checker(rule):
	  # this code runs once
	  # do something with rule['Consumes'] and rule['Requires']
	def check(state):
		# this code runs millions of times
		return True # or False
	
	return check

def make_effector(rule):
	# this code runs once
  	# do something with rule['Produces'] and rule['Consumes']
	def effect(state):
		# this code runs millions of times
		return next_state
	
	return effect


from collections import namedtuple
Recipe = namedtuple('Recipe',['name','check','effect','cost'])
all_recipes = []
for name, rule in Crafting['Recipes'].items():
	checker = make_checker(rule)
	effector = make_effector(rule)
	recipe = Recipe(name, checker, effector, rule['Time'])
	all_recipes.append(recipe)

def graph(state):
  for r in all_recipes:
    if r.check(state):
      yield (r.name, r.effect(state), r.cost)

def search(graph, initial, is_goal, limit, heuristic=None):
	from heapq import heappush, heappop

	prev = { initial:None }
	dist = { initial:0 }
	queue = [(0, initial)]
	inf = float('inf')
	total_cost = 0
	plan = []

	if(heuristic):
		heur = heuristic
	else:
		heur = lambda s: 0


	while queue:
		distCheck, state = heappop(queue)
		if distCheck == inf:
			break

		if is_goal(state):
			break

		currDist = dist[state]

		for name, next, cost in graph(state):
			alt = currDist + cost
			if next not in dist or alt < dist[next]:
				dist[next] = alt
				prev[next] = (name, state, cost)
				estimate = heur(next)
				heappush(queue, (alt + estimate, next))

	if is_goal(state):
		while prev[state] is not None:
			print '!!!!prev[state]: ', prev[state]
			plan.append(prev[state])
			total_cost += prev[state][2]
			state = prev[state]


	return total_cost, plan





t_initial = 'a'
t_limit = 20

edges = {'a': {'b':1,'c':10}, 'b':{'c':1}}

def t_graph(state):
	for next_state, cost in edges[state].items():
		yield ((state,next_state), next_state, cost)

def t_is_goal(state):
	return state == 'c'

def t_heuristic(state):
	return 0

print search(t_graph, t_initial, t_is_goal, t_limit, t_heuristic)


