import json

with open('Crafting.json') as f:
    Crafting = json.load(f)

"""print Crafting['Items']
print Crafting['Initial']
print Crafting['Goal']
print Crafting['Recipes']['craft stone_pickaxe at bench']"""

def inventory_to_tuple(d):
    """

    :rtype : object
    """
    return tuple(d.get(name, 0) for i, name in enumerate(Crafting['Items']))


def tuple_to_inventory(t):
    inventory = {}
    for i, name in enumerate(Crafting['Items']):
        if t[i] != 0:
            inventory[name] = t[i]
    return inventory


def make_initial_state(inventory):
    state = inventory_to_tuple(inventory)
    return state


def make_goal_checker(goal):
    newGoal = inventory_to_tuple(goal)
    checkList = []
    for i in range(len(newGoal)):
        if newGoal[i] != 0:
            checkList.append(i)
    def is_goal(state):
        #print "state",state
        #print "newGo",newGoal
        print 'state', state
        print checkList
        for each in checkList:
            if state[each] < newGoal[each]:
                return False
        return True

    return is_goal

def items_to_dict(d):
    item_indices = {}
    for i in range(len(d)):
        item_indices[d[i]] = i
    return item_indices

item_index = items_to_dict(Crafting['Items'])

def make_checker(rule):
    # this code runs once
    # do something with rule['Consumes'] and rule['Requires']
    consumes, requires = rule.get('Consumes',{}), rule.get('Requires',{})
    consumption_pairs = [(item_index[item],consumes[item]) for item in consumes]
    requirement_pairs = [(item_index[item], 1) for item in requires]
    both_pairs = consumption_pairs + requirement_pairs
    def check(state):
        # this code runs millions of times
        return all([state[i] >= v for i,v in both_pairs])

    return check


def make_effector(rule):
    # this code runs once
    # do something with rule['Produces'] and rule['Consumes']
    produces, consumes = rule.get('Produces',{}), rule.get('Consumes',{})
    production_pairs = [(item_index[item], produces[item]) for item in produces]
    print "prodpairs", production_pairs
    consumption_pairs = [(item_index[item], 1) for item in consumes]
    print "conspairs", consumption_pairs
    delta_pairs = production_pairs + consumption_pairs 
    #make this defined for all values in the state
    #get can return a default value
    #.get(something, 0) and enumerate(items) or something.
    #heur: return inf when more than some max limit of each item is produced
    #for all axe types unless goal requires that axe type, dont consider using it.
    def effect(state):
        # this code runs millions of times
        return tuple([state[i] + delta for i, delta in delta_pairs])

    return effect


from collections import namedtuple

Recipe = namedtuple('Recipe', ['name', 'check', 'effect', 'cost'])
all_recipes = []
for name, rule in Crafting['Recipes'].items():
    #print rule
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

    prev = {initial: None}
    dist = {initial: 0}
    queue = [(0, initial)]
    inf = float('inf')
    total_cost = 0
    plan = []

    if (heuristic):
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
            plan.append(prev[state])
            total_cost += prev[state][2]
            state = prev[state][1]

    return total_cost, plan

temp_goal = make_goal_checker(Crafting['Goal'])
initial = make_initial_state(Crafting['Initial'])

print search(graph, initial, temp_goal, 1000, None)
