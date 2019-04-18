import sys
from heapq import heappop, heappush, heapify
import math
from docopt import docopt
import collections

help = """
Usage:
  n_puzzle.py <argument_positionel> [<argument_positionel_optionel>] [--flag-optionel]
 
Options:
  -h --help          affiche help.
  -m                 manhattan heuristic.
  -o                 out of place heuritic.
  -l                 linear conflit heuristic.
  -u                 uniform cost heuristic.
  -g                 greedy search heuristic.
 
"""

def create_solved(N):
    it = 1
    number = N * N 
    x = 0 
    y = 0
    hg = hd = bg = bd = 0
    puzzle = []
    for i in range(0, N):
        puzzle.append([])
        for j in range(0, N):
            puzzle[i].append(0)
    while it < number:
        while x + hd < N and it < number:
            puzzle[y][x] = it
            x += 1 
            it += 1
        hg += 1
        x -= 1
        y += 1
        while y + bd < N and it < number:
            puzzle[y][x] = it
            y += 1
            it += 1
        hd += 1
        y -= 1
        x -= 1
        while x - bg >= 0 and it < number:
            puzzle[y][x] = it
            x -= 1
            it += 1
        bd += 1
        x += 1
        y -= 1
        while y - bd >= 0 and it < number:
            puzzle[y][x] = it
            y -= 1
            it += 1
        bg += 1
        y += 1
        x += 1
    return puzzle

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

def manhattan(grid,solved):
    result = 0
    for y, v in enumerate(grid):
        for x, value in enumerate(v):
            if grid[y][x] != solved[y][x] and value != 0:
                result += abs(y - dictOfGrid[value] // n) + abs(x - dictOfGrid[value] % n)
    return result

def out_of_place(grid, solved):
    result = 0
    for y, v in enumerate(grid):
        for x, value in enumerate(v):
            if grid[y][x] != solved[y][x] and value != 0:
                result += 1 
    return result

def rotate(grid, solved):
    r_grid = []
    for _ , v in enumerate(grid):
        r_grids = []
        for _ , value in enumerate(v):
            r_grids.append(value)
        r_grid.append(r_grids)
    r_grid = list(zip(*r_grid))
    r_solved = []
    for _ , v in enumerate(solved):
        r_solveds = []
        for _ , value in enumerate(v):
            r_solveds.append(value)
        r_solved.append(r_solveds)
    r_solved = list(zip(*r_solved))
    return r_grid, r_solved
    

def linear_conflict(grid, solved):
    result = 0
    for y, v in enumerate(grid):
        for x, _ in enumerate(v):
            if x + 1 == len(grid):
                break
            if grid[y][x] in solved[y] and grid[y][x + 1] in solved[y]:
                if grid[y][x] == solved[y][x + 1] or grid[y][x + 1] == solved[y][x]:
                    result += 1
    
    r_grid , r_solved = rotate(grid, solved)

    for y, v in enumerate(r_grid):
        for x, _ in enumerate(v):
            if x + 1 == len(r_grid):
                break
            if r_grid[y][x] in r_solved[y] and r_grid[y][x + 1] in r_solved[y]:
                if r_grid[y][x] == r_solved[y][x + 1] or r_grid[y][x + 1] == r_solved[y][x]:
                    result += 1
    return result

def reconstruct_path(node):
    res = []
    moves = 0
    while node.parent != None:
        res.insert(0, node.grid)
        node = node.parent
        moves += 1
    return res, moves

def h(child, solved, heuristic):
    if heuristic == 'm' or heuristic is None:
        return manhattan(child, solved)
    if heuristic == 'o':
        return manhattan(child, solved) + out_of_place(child, solved)
    if heuristic == 'l':
        return manhattan(child, solved) + linear_conflict(child, solved)
    if heuristic == 'u':
        return manhattan(child, solved)
    if heuristic == 'g':
        return manhattan(child, solved)

def solve(data, solved, heuristic):
    tot_number_of_states = 0
    start = Node(None, data)
    open_l = []
    closed = []
    closedMap_set = set(closed)
    openMap_set = {start.__hash__: start}
    heappush(open_l, start)
    max_size = 1
    while open_l:
        max_size = max(max_size, len(open_l))
        current = heappop(open_l)
        tot_number_of_states += 1
        closed.append(current)
        closedMap_set.add(current)

        if current.grid == solved:
            path, moves = reconstruct_path(current)
            print('the complexity in time is {}'.format(tot_number_of_states))
            print('number of moves is {}'.format(moves))
            print('the complexity in size is {}'.format(max_size))
            return path
        
        for child in getChild(current.grid):
            child_node = Node(current, child)
    
            if child_node in closedMap_set:
                continue
    
            child_node.g = current.g + 1
            child_node.h = h(child, solved, heuristic)
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
                
def is_solvable(N, data, dictfGrid):
    solved_grid = {}
    data_grid = {}
    data_grid2 = {}
 
    for k, v in dictOfGrid.items():
        solved_grid.update({k: (v // N, v % N)})
    flat_data = [n for lists in data for n in lists]
    dictOfGridData = {flat_data[i] : dictOfGrid[flat_data[i]] for i in range(0,len(flat_data))}
    dictOfGridData2 = {flat_data[i] : i for i in range(0,len(flat_data))}
    for k, v in dictOfGridData2.items():
        data_grid2.update({k: (v // N, v % N)})
    
    for k, v in dictOfGridData.items():
       data_grid.update({k: (v // N, v % N)})
    
    sorted_solved = collections.OrderedDict(sorted(solved_grid.items()))
    sorted_data = collections.OrderedDict(sorted(data_grid2.items()))

    inversion = 0
    pos = 0
    for k in dictOfGridData.keys():
        if k != 0:
            for i in range(pos + 1, len(dictOfGridData)):
                if flat_data[i] != 0:
                    if dictOfGridData[k] > dictOfGridData[flat_data[i]]:
                        inversion += 1 
            pos += 1
    if N % 2 != 0:
        if inversion % 2 == 0:
            return True
    else:
        blank_row_pos = abs(sorted_solved[0][0] - sorted_data[0][0]) + 1
        if blank_row_pos % 2 == 0 and inversion % 2 != 0:
            return True
        if blank_row_pos% 2 != 0 and inversion % 2 == 0:
            return True
    return False    


#d = solve(data, solved)

def create_solved(N):
    it = 1
    number = N * N 
    x = 0 
    y = 0
    hg = hd = bg = bd = 0
    puzzle = []
    for i in range(0, N):
        puzzle.append([])
        for j in range(0, N):
            puzzle[i].append(0)
    while it < number:
        while x + hd < N and it < number:
            puzzle[y][x] = it
            x += 1 
            it += 1
        hg += 1
        x -= 1
        y += 1
        while y + bd < N and it < number:
            puzzle[y][x] = it
            y += 1
            it += 1
        hd += 1
        y -= 1
        x -= 1
        while x - bg >= 0 and it < number:
            puzzle[y][x] = it
            x -= 1
            it += 1
        bd += 1
        x += 1
        y -= 1
        while y - bd >= 0 and it < number:
            puzzle[y][x] = it
            y -= 1
            it += 1
        bg += 1
        y += 1
        x += 1

    return puzzle

if __name__ == '__main__':
    arguments = docopt(help)

    if arguments['<argument_positionel_optionel>'] not in ['m', 'o', 'l', 'u', 'g'] and arguments['<argument_positionel_optionel>']:
        print(help)
        sys.exit(0)
    with open(sys.argv[1]) as f:
        data = f.readlines()
   
    data = [x.strip() for x in data]
    N = int(data[1])
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
    
    solved = create_solved(int(N))

    flat_solved = [n for lists in solved for n in lists]
    dictOfGrid = {flat_solved[i] : i for i in range(0,len(flat_solved))}

    flat_data = [n for lists in data for n in lists]
    dictOfGridData = {flat_data[i] : i for i in range(0,len(flat_data))}

    n = math.sqrt(len(flat_solved))

    if is_solvable(N, data, dictOfGrid):
        puzzle = solve(data, solved, arguments['<argument_positionel_optionel>'])
    else:
        print('unsolvable')
        sys.exit(0)

    printer(data)
    print('------------------')

    for p in puzzle:
        printer(p)
        print('\n')