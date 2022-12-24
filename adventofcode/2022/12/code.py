
class Node:
  def __init__(self, pos, height):
    self.pos = pos
    self.height = height
    self.neighbors = []
    self.visited = False
    self.isend = False
    self.isstart = False
    self.parent = None
  def get_position(self):
    return self.pos
  def get_height(self):
    return self.height
  def add_neighbor(self, node):
    self.neighbors.append(node)
  def get_neighbors(self):
    return self.neighbors
  def get_parent(self):
    return self.parent
  def set_visited(self):
    self.visited = True
  def set_parent(self, node):
    self.parent = node
  def set_isend(self):
    self.isend = True
  def set_isstart(self):
    self.isstart = True


def find_neighbors(g: list, n: Node)->None:
  r, c = n.get_position()
  #for r1, c1 in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
  for r1, c1 in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
    if r + r1 >= 0 and c + c1 >= 0 and r + r1 < len(g) and c + c1 < len(g[0]):
      if not g[r+r1][c+c1].visited:
        n.add_neighbor(g[r+r1][c+c1])


def check_path(grid: list, spos: tuple):

  # Create queue
  start_position = spos
  queue = []
  queue.insert(0, grid[start_position[0]][start_position[1]])
  cur_node = None

  while queue:
    cur_node = queue.pop()
    cur_node.set_visited()
    if cur_node.isend:
      break
    find_neighbors(grid, cur_node)
    for neighbor in cur_node.get_neighbors():
      if not neighbor.visited and neighbor.get_height() <= cur_node.get_height() + 1:
        neighbor.set_visited()
        neighbor.set_parent(cur_node)
        queue.insert(0, neighbor)

  if not cur_node.isend:
    raise ValueError("We didn't reach end node")


  #print(f"Current node is the end {cur_node.get_position()}")
  #while cur_node.get_parent() is not None:
  #  cur_node = cur_node.get_parent()
  #  print(f"Current node {cur_node.get_position()}")
  #  #input()
  #exit()

  # Create vizualization grid
  vgrid = [['.' for j in range(len(grid[0]))] for i in range(len(grid))]

  # Get path
  steps = 0
  end_node = cur_node
  path_positions = []
  vgrid[end_node.get_position()[0]][end_node.get_position()[1]] = 'E'
  while cur_node.get_parent() is not None:
    path_positions.insert(0, cur_node.get_position())
    steps += 1
    cur_node = cur_node.get_parent()
    vgrid[cur_node.get_position()[0]][cur_node.get_position()[1]] = 'o'
  vgrid[grid[start_position[0]][start_position[1]].get_position()[0]][grid[start_position[0]][start_position[1]].get_position()[1]] = 'S'

  # Print grid
  #for r in vgrid:
  #  print(*r, sep='')

  return cur_node.get_position(), end_node.get_position(), steps


def create_grid(start_position: tuple)->list:

  heights = 'abcdefghijklmnopqrstuvwxyz'

  grid = []
  for x, line in enumerate(open('input.txt').readlines()):
    grid.append([])
    n = None
    for y, char in enumerate(list(line.strip())):
      if char == 'S':
        if (x, y) == start_position:
          n = Node((x, y), heights.index('a'))
          n.set_isstart()
        else:
          n = Node((x, y), heights.index('a'))
      elif char == 'E':
        n = Node((x, y), heights.index('a'))
        n.set_isend()
      else:
        n = Node((x, y), heights.index(char))
      grid[x].append(n)

  return grid


def main():

  start_position = (0, 0)
  grid = create_grid(start_position)

  start, end, steps = check_path(grid, start_position)
  print(f"Part 1: from {start} to {end} took {steps} steps")
  # Result: 420

  # Check `a` heights in grid
  start_points = []
  for x, row in enumerate(grid):
    for y, node in enumerate(grid[x]):
      if grid[x][y].get_height() == 0:
        start_points.append(grid[x][y].get_position())

  steps_count = set()
  for p in start_points:
    g = create_grid(p)
    try:
      start, end, steps = check_path(g, p)
    except ValueError:
      pass

    if not start == end:
      steps_count.add(steps)

  print(f"Part 2: shortest path is {min(steps_count)}")
  # Result: 414

main()
