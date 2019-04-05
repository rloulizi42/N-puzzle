import sys
from heapq import heappop, heappush, heapify

with open(sys.argv[1]) as f:
    data = f.readlines()
data = [x.strip() for x in data]
n = data[1]
data = [list(x.replace(" ", "")) for x in data[2:]]
data = [list(map(int, x)) for x in data]

solved = [[1, 2, 3],
          [8, 0, 4],
          [7, 6, 5]]

DOWN = (-1, 0)
UP = (1, 0)
LEFT = (0, 1)
RIGHT = (0, -1)

def can_move(dir, grid, x1, y1):
    y = y1 + dir[0]
    x = x1 + dir[1]
    if y < 0 or x < 0 or x > len(grid) or y > len(grid):
        return 0
    return 1

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

def printer(grid):
    for line in grid:
        print(line)

def getChild(grid):
    childs = []
    for m in [DOWN, UP, LEFT, RIGHT]:
        child = move(m, grid)
        if child != grid:
            childs.append(child)
    return childs


class Node():
    def __init__(self, parent=None):
        self.parent = parent
        self.grid = []
        
        self.g = 0
        self.h = 0
        self.f = 0

mv_list = []

def h(grid,solved):
    result = 0
    for y, v in enumerate(grid):
        for x, value in enumerate(v):
            if grid[y][x] != solved[y][x] and value == 0:
                result += 1
    return result

def g(grid)

def solve(data, solved):
    Node start = data.
    open_set = [data]
    closed_set = []
    heapify(open_set)
    heapify(closed_set)
    while open_set:
        current = heappop(open_set)
        heappush(closed_set, current)
        if current == solved:
      #     return
        for child in getChild(current):
            curr_s = Node(child)
            if curr_s in closed_set:
                
#        if (curr == solved):
#            reconstruct_path
    
#solve(data, solved)
#a = Node()
#a.h = 42
#b = Node()
#b.h = 21

heap = []
#heappush(heap, (a.h, a))
#heappush(heap, (b.h, b))
#while heap:
 #    print(heappop(heap)[0])

print('initial')
printer(solved)
print('')

c = getChild(solved)
for chil in c:
    printer(chil)
    print('\n')