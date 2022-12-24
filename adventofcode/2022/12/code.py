
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
  for r1, c1 in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
    if r + r1 >= 0 and c + c1 >= 0 and r + r1 < len(g) and c + c1 < len(g[0]):
      if not g[r+r1][c+c1].visited:
        n.add_neighbor(g[r+r1][c+c1])

def main():
  heights = 'abcdefghijklmnopqrstuvwxyz'

  # Create objects in grid
  grid = []
  for x, line in enumerate(open('input.txt').readlines()):
    grid.append([])
    n = None
    for y, char in enumerate(list(line.strip())):
      if char == 'S':
        n = Node((x, y), heights.index('a'))
        n.set_isstart()
      elif char == 'E':
        n = Node((x, y), heights.index('a'))
        n.set_isend()
      else:
        n = Node((x, y), heights.index(char))
      grid[x].append(n)

  # Create queue
  queue = []
  queue.append(grid[20][0])
  cur_node = None

  while queue:
    cur_node = queue.pop()
    cur_node.set_visited()
    print(f"- Current node {cur_node.get_position()} height [{cur_node.get_height()}]")
    if cur_node.isend:
      print(f"End node")
      break
    find_neighbors(grid, cur_node)
    for neighbor in cur_node.get_neighbors():
      print(f"  - Neighbor: {neighbor.get_position()}")
      if not neighbor.visited and neighbor.get_height() <= cur_node.get_height() + 1:
        neighbor.set_visited()
        neighbor.set_parent(cur_node)
        queue.insert(0, neighbor)

  # Get path
  print(f"Node {cur_node.get_position()}")
  steps = 0
  while not cur_node.isstart:
    steps += 1
    cur_node = cur_node.get_parent()
  print(f"Part 1: {steps}")

main()
