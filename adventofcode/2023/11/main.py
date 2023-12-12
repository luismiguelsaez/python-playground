from sys import argv
from itertools import combinations
from ray.util.multiprocessing import Pool

## Part 1
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

# Galaxies after expanded rows and columns

#  . . . . # . . . . . . . .
#  . . . . . . . . . # . . .
#  # . . . . . . . . . . . .
#  . . . . . . . . . . . . .
#  . . . . . . . . . . . . .
#  . . . . . . . . # . . . .
#  . # . . . . . . . . . . .
#  . . . . . . . . . . . . #
#  . . . . . . . . . . . . .
#  . . . . . . . . . . . . .
#  . . . . . . . . . # . . .
#  # . . . . # . . . . . . .

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

## Part 2

grid = [list(r.rstrip()) for r in open(argv[1], 'r').readlines()]

# Check empty rows and columns
empty_rows = [r for r in range(len(grid))]
empty_cols = [r for r in range(len(grid[0]))]

for x in range(len(grid)):
    for y in range(len(grid[x])):
        if grid[x][y] == '#':
            empty_rows.remove(x) if x in empty_rows else False
            empty_cols.remove(y) if y in empty_cols else False

# Find galaxies
galaxies = []
for x in range(len(grid)):
    for y in range(len(grid[x])):
        if grid[x][y] == '#':
            galaxies.append((x, y))

galaxy_pairs = list(combinations(galaxies, 2))

# Galaxies with rows and cols cross lines

#  . . | # . | . . | .
#  . . | . . | . # | .
#  # . | . . | . . | .
#  - - + - - + - - + -
#  . . | . . | # . | .
#  . # | . . | . . | .
#  . . | . . | . . | #
#  - - + - - + - - + -
#  . . | . . | . # | .
#  # . | . # | . . | .

get_distance = lambda pair: abs(pair[0][0] - pair[1][0]) + abs(pair[0][1] - pair[1][1])

total = 0
for pair in galaxy_pairs:
    crossed_cols = [c for c in empty_cols if pair[0][1] <= c <= pair[1][1] or pair[1][1] <= c <= pair[0][1]]
    crossed_rows = [r for r in empty_rows if pair[0][0] <= r <= pair[1][0] or pair[1][0] <= r <= pair[0][0]]
    linear_dist = get_distance(pair)
    total_distance = linear_dist + ( len(crossed_cols) * 1_000_000 ) + ( len(crossed_rows) * 1_000_000 ) - len(crossed_cols) - len(crossed_rows)
    total += total_distance

print(f"Part two: {total}")
