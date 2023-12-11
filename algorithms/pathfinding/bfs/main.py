class Node():
    def __init__(self, coord, parent):
        self.coord = coord
        self.parent = parent
    def __repr__(self):
        return f"{self.parent.coord} -> {self.coord}"

find_neighbors_diagonals = lambda x, y, height, width: list(filter(lambda p: 0 <= p[0] < height and
                                                                             0 <= p[1] < width
                                                                             and (p[0] != x or p[1] != y),
                                                                             [ (i, j) for i in range(x-1, x+2) for j in range(y-1, y+2) ]))

find_neighbors = lambda x, y, height, width: list(filter(lambda p: 0 <= p[0] < height and
                                                                   0 <= p[1] < width
                                                                   and (p[0] != x or p[1] != y),
                                                                   [ (i+x, j+y) for i,j in [(-1,0),(0,-1),(0,1),(1,0)] ]))

def find_path(grid, start, end):
    visited = [start]
    queue = [Node(start, ())]
    while len(queue) > 0:
        cur = queue.pop()
        if cur.coord == end:
            break
        neigh = find_neighbors_diagonals(cur.coord[0], cur.coord[1], len(grid), len(grid[0]))
        for n in neigh:
            if n not in visited:
                node = Node(n, cur)
                queue.insert(1, node)
                visited.append(n)

    steps = 0
    while cur.coord != start:
        cur = cur.parent
        steps += 1
    
    return steps
