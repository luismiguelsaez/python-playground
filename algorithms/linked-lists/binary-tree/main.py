
class Node:
  def __init__(self, value):
    self.value = value
    self.left = None
    self.right = None

  def set_left(self, n):
    self.left = n

  def set_right(self, n):
    self.right = n


def main() -> None:

  # Create binary tree nodes
  a = Node('a')
  b = Node('b')
  c = Node('c')
  d = Node('d')
  e = Node('e')
  f = Node('f')
  g = Node('g')

  # Link nodes
  a.set_left(b)
  a.set_right(c)
  b.set_left(d)
  b.set_right(e)
  c.set_left(f)
  c.set_right(g)

  # Discover tree nodes starting from root
  queue = [a]
  while queue:
    current = queue.pop()
    print(f"Checking node {current.value}, queue length is {len(queue)}")
    if current.left is not None: queue.insert(0, current.left)
    if current.right is not None: queue.insert(0, current.right)


main()
