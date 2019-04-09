import sys
from heapq import heappop, heappush, heapify

with open(sys.argv[1]) as f:
    data = f.readlines()
data = [x.strip() for x in data]
n = data[1]
data = [list(x.replace(" ", "")) for x in data[2:]]
data = [list(map(int, x)) for x in data]

DOWN = (-1, 0)
UP = (1, 0)
LEFT = (0, 1)
RIGHT = (0, -1)

def can_move(dir, grid, x1, y1):
    y = y1 + dir[0]
    x = x1 + dir[1]
    if y < 0 or x < 0 or x >= len(grid) or y >= len(grid):
        return 0
    return 1

def printer(grid):
    for line in grid:
        print(line)

def move(dir, grid):
    grid_all = []
    y1 = x1 = 0
    for y, v in enumerate(grid):
        grids = []
        for x, value in enumerate(v):
            if value == 0:
                y1 = y
                x1 = x
            grids.append(value)
        grid_all.append(grids)
    if can_move(dir, grid, x1, y1):
        grid_all[y1][x1] = grid[y1 + dir[0]][x1 + dir[1]]
        grid_all[y1 + dir[0]][x1 + dir[1]] = 0
    return grid_all

def getChild(grid):
    childs = []
    for m in [DOWN, UP, LEFT, RIGHT]:
        child = move(m, grid)
        if child != grid:
            childs.append(child)
    return childs


class Node():
    def __init__(self, parent=None, grid=None):
        self.parent = parent
        self.grid = grid
        
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        if(self.f < other.f):
            return True
        else:
            return False

def getCoord(solved, value, b):
    for y, v in enumerate(solved):
        for x, v1 in enumerate(v):
            if value == v1:
                if b:
                    return y
                else:
                    return x
    return 0

def h(grid,solved):
    result = 0
    for y, v in enumerate(grid):
        for x, value in enumerate(v):
            if grid[y][x] != solved[y][x] and value == 0:
                result += abs(y - getCoord(solved, grid[y][x], True)) + abs(x - getCoord(solved, grid[y][x], False))
    return result

def reconstruct_path(node):
    res = []
    while node.parent != None:
        res.insert(0, node.grid)
        node = node.parent
    return res

def solve(data, solved):
    start = Node(None, data)
    open_set = []
    closed_set = []
    closedMap_set = set(closed_set)
    openMap_set = set(open_set)
    heappush(open_set, start)
    while open_set:
        current = heappop(open_set)
        closed_set.insert(0, current)
        closedMap_set.add(current)
        if current.grid == solved:
            path = reconstruct_path(current)
            path.insert(0,data)
            return path
        for child in getChild(current.grid):
            child_node = Node(current, child)
            if child_node in closedMap_set:
                continue
            child_node.g = current.g + 1
            child_node.h = h(child, solved)
            child_node.f = child_node.g + child_node.h
            if child_node in openMap_set and child_node.f < open_node.f:
                continue
            heappush(open_set, child_node)
            openMap_set.add(child_node)
    print('No Solution')
                
solved = [[1, 2, 3],
          [8, 0, 4],
          [7, 6, 5]]

data1 =  [[1, 2, 3],
          [7, 8, 4],
          [0, 6, 5]]

c = solve(data, solved)

for e in c:
    print('')
    printer(e)