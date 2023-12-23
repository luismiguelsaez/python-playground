from sys import argv
from time import sleep

grid = [list(l.rstrip()) for l in open(argv[1], 'r').readlines()]

find_neighbors = lambda x, y, height, width: list(filter(lambda p: 0 <= p[0] < height and
                                                                   0 <= p[1] < width
                                                                   and (p[0] != x or p[1] != y),
                                                                   [ (i+x, j+y) for i,j in [(0,1), (1,0),(0,-1),(-1,0)] ]))

class Node:
    def __init__(self, coord, value, distance):
        self.coord = coord
        self.value = int(value)
        self.distance = distance
        self.visited = False
    def __repr__(self):
        return f"{self.value} <-> {self.distance}"

nodes = [ [ Node((r, c), grid[r][c], float('infinity')) for c in range(len(grid[r])) ] for r in range(len(grid)) ]
nodes[0][0].distance = 0

queue = [nodes[0][0]]
while len(queue) != 0:
    node = queue.pop(0)
    nodes[node.coord[0]][node.coord[1]].visited = True
    #grid[node.coord[0]][node.coord[1]] = 'x'
    neighbors = find_neighbors(node.coord[0], node.coord[1], len(nodes), len(nodes[0]))
    print(f"Node val: {node.value} at {node.coord} distance: {node.distance} neighbors: {neighbors}")
    for n in neighbors:
        if not nodes[n[0]][n[1]].visited:
            print(f"  - Neighbor value: {grid[n[0]][n[1]]} at {n} was not visited")
            ndis = node.value + node.distance
            if ndis < nodes[n[0]][n[1]].distance:
                print(f"  - Updating neighbor at {n} distance: {ndis} < {nodes[n[0]][n[1]].distance}")
                nodes[n[0]][n[1]].distance = ndis
                queue.append(nodes[n[0]][n[1]])
                grid[n[0]][n[1]] = f"[{ndis}]"
            else:
                print(f"  - Not updating neighbor at {n} distance: {ndis} > {nodes[n[0]][n[1]].distance}")
    for r in grid: print(*r)
    #sleep(1)