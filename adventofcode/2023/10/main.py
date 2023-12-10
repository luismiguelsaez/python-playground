from sys import argv
from time import sleep

grid = [list(r.rstrip()) for r in open(argv[1], 'r').readlines()]

pipes = {
    '|': [(1, 0), (-1, 0)],
    '-': [(0, 1), (0, -1)],
    'L': [(0, 1), (-1, 0)],
    'J': [(-1, 0), (0, -1)],
    '7': [(1, 0), (0, -1)],
    'F': [(0, 1), (1, 0)]
}

start = [ (r, c) for r in range(len(grid)) for c in range(len(grid[r])) if grid[r][c] == 'S' ][0]

def find_adj(grid, point):
    points = []
    for x, y in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
        cpoint = ( point[0] + x, point[1] + y )
        if cpoint[0]>=0 and cpoint[1]>=0 and cpoint[0]<len(grid) and cpoint[1]<len(grid[0]):
                points.append(cpoint)
    return points

class point():
    def __init__(self, coord, parent):
        self.coord = coord
        self.parent = parent
    def get_coord(self):
        return self.coord
    def get_parent(self):
        return self.parent

queue = [point(start, ())]
visited = []
while len(queue) > 0:
    cur = queue.pop()
    cur_coord = cur.get_coord()
    if cur_coord == start:
        if cur_coord not in visited:
            adj_points = find_adj(grid, cur_coord)
            for p in adj_points:
                pipe = grid[p[0]][p[1]]
                if pipe in pipes:
                    for e in pipes[pipe]:
                        if ( cur_coord[0] - e[0], cur_coord[1] - e[1] ) == p:
                            queue.append(point(p, cur))
                            visited.append(cur_coord)
    else:
        pipe = grid[cur_coord[0]][cur_coord[1]]
        parent = cur.get_parent()
        parent_coord = parent.get_coord()
        directions = list(filter(lambda x: ( cur_coord[0] - parent_coord[0], cur_coord[1] - parent_coord[1] ) != (x[0] * -1, x[1] * -1), pipes[pipe]))
        direction = directions[0]
        next_coord = (cur_coord[0] + direction[0], cur_coord[1] + direction[1])
        if next_coord != start:
            queue.append(point(next_coord, cur))
            visited.append(cur_coord)

print(f"Part one: {round(len(set(visited)) / 2)}")
