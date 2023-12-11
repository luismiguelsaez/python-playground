from sys import argv
from itertools import combinations
from ray.util.multiprocessing import Pool

grid = [list(r.rstrip()) for r in open(argv[1], 'r').readlines()]

# Check empty rows and columns
empty_rows = [r for r in range(len(grid))]
empty_cols = [r for r in range(len(grid[0]))]

for x in range(len(grid)):
    for y in range(len(grid[x])):
        if grid[x][y] == '#':
            empty_rows.remove(x) if x in empty_rows else False
            empty_cols.remove(y) if y in empty_cols else False

# Insert additional rows and columns
for count, r in enumerate(empty_rows):
    grid.insert(r + count, ['.' for _ in range(len(grid[0]))])

for r in range(len(grid)):
    for count, c in enumerate(empty_cols):
        grid[r].insert(c + count, '.')

# Find galaxies
galaxies = []
for x in range(len(grid)):
    for y in range(len(grid[x])):
        if grid[x][y] == '#':
            galaxies.append((x, y))

# Calculate distances
galaxy_pairs = list(combinations(galaxies, 2))
paths_sum = sum(map(lambda x: abs(x[0][0] - x[1][0]) + abs(x[0][1] - x[1][1]), combinations(galaxies, 2)))

print(f"Part one: {paths_sum}")
