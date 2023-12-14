from sys import argv

grid = [list(l.rstrip()) for l in open(argv[1], 'r').readlines()]

def move_rock_up(grid, x, y):
    while grid[x - 1][y] not in ['#', 'O'] and x - 1 >= 0:
        x = x - 1
        grid[x][y] = 'O'
        grid[x+1][y] = '.'
    return (x, y)

total = 0
for r in range(len(grid)):
    for c in range(len(grid[0])):
        if grid[r][c] == 'O':
            pos = move_rock_up(grid, r, c)
            total += len(grid) - pos[0]

for r in grid: print(*r, sep='')

print(f"Part one: {total}")
