import sys
from heapq import heappop, heappush, heapify
import math

with open(sys.argv[1]) as f:
    data = f.readlines()
data = [x.strip() for x in data]
N = data[1]
data = [list(x.split(" ")) for x in data[2:]]

new_data = []

for lignes in data:
    l = []
    for x in lignes:
        if x.isdigit():
            l.append(x)
    new_data.append(l)

data = new_data
data = [list(map(int, x)) for x in data]

DOWN = (-1, 0)
UP = (1, 0)
LEFT = (0, 1)
RIGHT = (0, -1)

solved = [[1, 2, 3, 4],
          [12, 13, 14, 5],
          [11, 0, 15, 6],
          [10,9, 8, 7]]

flat_solved = [n for lists in solved for n in lists]
dictOfGrid = {flat_solved[i] : i for i in range(0,len(flat_solved))}
n = math.sqrt(len(flat_solved))

def printer(grid):
    for line in grid:
        print(line)

def move(dir, grid):
    grid_all = []
    y1 = x1 = yy = xx = 0
    for y, v in enumerate(grid):
        grids = []
        for x, value in enumerate(v):
            if value == 0:
                y1 = y + dir[0]
                x1 = x + dir[1]
                yy = y
                xx = x
            grids.append(value)
        grid_all.append(grids)
    if not (y1 < 0 or x1 < 0 or x1 >= n or y1 >= n):
        grid_all[yy][xx] = grid[y1][x1]
        grid_all[y1][x1] = 0
    return grid_all

def getChild(grid):
    childs = []
    for m in [DOWN, UP, LEFT, RIGHT]:
        child = move(m, grid)
        if child != grid:
            childs.append(child)
    return childs


class Node():
    def __init__(self, parent=None, grid=None, f=0):
        self.parent = parent
        self.grid = grid
        
        self.g = 0
        self.h = 0
        self.f = 0

    def __hash__(self):
        e = [n for lists in self.grid for n in lists]
        return hash(tuple(e))

    def __ne__(self, other):
        if self is None or other is None:
            return True
        if self.grid == other.grid:
            return False
        else:
            return True

    def __eq__(self, other):
        if self.grid == other.grid:
            return True
        else:
            return False

    def __lt__(self, other):
        if(self.f < other.f):
            return True
        else:
            return False

def h(grid,solved):
    result = 0
    for y, v in enumerate(grid):
        for x, value in enumerate(v):
            if grid[y][x] != solved[y][x] and value != 0:
                result += abs(y - dictOfGrid[value] // n) + abs(x - dictOfGrid[value] % n)
    return result

def reconstruct_path(node):
    res = []
    while node.parent != None:
        res.insert(0, node.grid)
        node = node.parent
    return res

def solve(data, solved):
    start = Node(None, data)
    open_l = []
    closed = []
    closedMap_set = set(closed)
    openMap_set = {start.__hash__: start}
    heappush(open_l, start)
    while open_l:
        current = heappop(open_l)
        closed.append(current)
        closedMap_set.add(current)
        
        if current.grid == solved:
            path = reconstruct_path(current)
            return path
        
        for child in getChild(current.grid):
            child_node = Node(current, child)
    
            if child_node in closedMap_set:
                continue
    
            child_node.g = current.g + 1
            child_node.h = h(child, solved)
            child_node.f = child_node.g + child_node.h

            if child_node in openMap_set.values():
                tmp = openMap_set[child_node.__hash__]
    
                if child_node.f < tmp.f:
                    tmp.parent = child_node.parent
                    tmp.f = child_node.f
                    tmp.g = child_node.g
                    tmp.h = child_node.h
                    continue

            heappush(open_l, child_node)
            openMap_set.update({child_node.__hash__:child_node})

    print('No Solution')
                
#puzzle = solve(data, solved)

#print('la piece a resoudre')
#printer(data)

#print('---------')

#for n in puzzle:
#    printer(n)
#    print('\n')

#print('la piece ci dessus est la piece resolu l\'aziz')

import collections

def is_solvable(N, data, dictOfGrid):
    solved_grid = {}
    data_grid = {}
 
    for k, v in dictOfGrid.items():
        solved_grid.update({k: (v // N, v % N)})
    flat_data = [n for lists in data for n in lists]
    dictOfGridData = {flat_data[i] : i for i in range(0,len(flat_data))}
    for k, v in dictOfGridData.items():
        data_grid.update({k: (v // N, v % N)})
    
    sorted_solved = collections.OrderedDict(sorted(solved_grid.items()))
    sorted_data = collections.OrderedDict(sorted(data_grid.items()))

    inversion = 0
    print(sorted_data)
    print(sorted_solved)
    for i, _ in enumerate(sorted_data):
        inversion += abs(sorted_solved[i][0] - sorted_data[i][0]) + abs(sorted_solved[i][1] - sorted_data[i][1])
    
    print(inversion)

    if N % 2 != 0:
        if inversion % 2 == 0:
            return True
    else:
        blank_row_pos = abs(sorted_solved[0][0] - sorted_data[0][0])
        print(blank_row_pos)
        if blank_row_pos == 0:
            return True
        if blank_row_pos % 2 == 0 and inversion % 2 != 0:
            return True
        if blank_row_pos % 2 != 0 and inversion % 2 == 0:
            return True
    return False    


#d = solve(data, solved)

inversion = is_solvable(int(N), data, dictOfGrid)
printer(solved)
print('\n')
printer(data)
print(inversion)