from sys import argv
from itertools import cycle
from time import sleep
import copy
import os

# Part 1
grid = [list(l.rstrip()) for l in open(argv[1], 'r').readlines()]

def move_rock_up(grid, x, y):
    while grid[x - 1][y] not in ['#', 'O'] and x - 1 >= 0:
        x = x - 1
        grid[x][y] = 'O'
        grid[x+1][y] = '.'
    return (x, y)

def move_rocks_right(grid):
    for c in range(len(grid[0]) - 1, -1, -1):
        for r in range(len(grid)):
            if grid[r][c] == 'O':
                x = r
                y = c
                while y + 1 < len(grid[0]) and grid[x][y + 1] not in ['#', 'O']:
                    y = y + 1
                    grid[x][y] = 'O'
                    grid[x][y-1] = '.'

def move_rocks_left(grid):
    for c in range(len(grid[0])):
        for r in range(len(grid)):
            if grid[r][c] == 'O':
                x = r
                y = c
                while y - 1 >= 0 and grid[x][y - 1] not in ['#', 'O']:
                    y = y - 1
                    grid[x][y] = 'O'
                    grid[x][y+1] = '.'

def move_rocks_up(grid):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 'O':
                x = r
                y = c
                while x - 1 >= 0 and grid[x - 1][y] not in ['#', 'O']:
                    x = x - 1
                    grid[x][y] = 'O'
                    grid[x+1][y] = '.'

def move_rocks_down(grid):
    for r in range(len(grid) - 1, -1, -1):
        for c in range(len(grid[0])):
            if grid[r][c] == 'O':
                x = r
                y = c
                while x + 1 < len(grid) and grid[x + 1][y] not in ['#', 'O']:
                    x = x + 1
                    grid[x][y] = 'O'
                    grid[x-1][y] = '.'

total = 0
for r in range(len(grid)):
    for c in range(len(grid[0])):
        if grid[r][c] == 'O':
            pos = move_rock_up(grid, r, c)
            total += len(grid) - pos[0]

print(f"Part one: {total}")

## Part 2
grid = [list(l.rstrip()) for l in open(argv[1], 'r').readlines()]

cycles_start_repeat = -1
cycles_repeat_hist = []
grid_hash = hash(tuple([hash(tuple(r)) for r in grid]))
grid_hashes = [grid_hash]
mod_grid = copy.deepcopy(grid)
count = 0
cycles = 0
calc_cycles = 0
for c in cycle(['up', 'left', 'down', 'right']):
    match c:
        case 'up':
            move_rocks_up(mod_grid)
        case 'left':
            move_rocks_left(mod_grid)
        case 'down':
            move_rocks_down(mod_grid)
        case 'right':
            move_rocks_right(mod_grid)

    count += 1
    cycles += 1 if count % 4 == 0 else 0 

    mod_grid_hash = hash(tuple([hash(tuple(r)) for r in mod_grid]))
    if mod_grid_hash in grid_hashes:
        if cycles_start_repeat == -1:
            cycles_start_repeat = cycles
            grid_hashes = []
        else:
            if len(cycles_repeat_hist) < 2:
                cycles_repeat_hist.append(cycles)
                grid_hashes = []
            else:
                calc_cycles = cycles_start_repeat + ( 1_000_000_000 - cycles_start_repeat ) % ( cycles_repeat_hist[1] - cycles_repeat_hist[0] )
                #print(f"Cycles to solution: {calc_cycles}")
                break

    grid_hashes.append(mod_grid_hash)

    #if cycles == 168: # Valid total
    if cycles == 1_000_000_000:
        break

mod_grid = copy.deepcopy(grid)
count = 0
cycles = 0
for c in cycle(['up', 'left', 'down', 'right']):
    match c:
        case 'up':
            move_rocks_up(mod_grid)
        case 'left':
            move_rocks_left(mod_grid)
        case 'down':
            move_rocks_down(mod_grid)
        case 'right':
            move_rocks_right(mod_grid)

    count += 1
    cycles += 1 if count % 4 == 0 else 0

    if cycles == calc_cycles:
        break

total = 0
for r in range(len(mod_grid)):
    for c in range(len(mod_grid[0])):
        if mod_grid[r][c] == 'O':
            total += len(mod_grid) - r

# Print final grid
#for r in grid: print(*r, sep='')

print(f"Part two: {total}")
