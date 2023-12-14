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

mod_grid = copy.deepcopy(grid)
count = 0
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
    
    # Print grid
    os.system('clear')
    for r in mod_grid: print(*r, sep='')

    e = 0
    for rm in range(len(mod_grid)):
        if mod_grid[rm] == grid[rm]: e += 1
    if e == len(mod_grid):
        print(f"Cycle repeats at iteration {count}")
        break

    if count == 1_000_000_000:
        break


for r in grid: print(*r, sep='')
