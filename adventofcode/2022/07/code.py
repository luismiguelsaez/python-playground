import string

class Node:
  def __init__(self, name: str, is_dir: bool = False, is_root: bool = False, size: int = 0):
    self.name = name
    self.is_dir = is_dir
    self.is_root = is_root
    if is_dir:
      self.children = []
    else:
      self.size = size
  def add_child(self, n):
    self.children.append(n)
  def set_parent(self, n):
    self.parent = n
  def get_parent(self):
    return self.parent
  def get_path(self):
    path = []
    n = self
    while n.name != '/':
      path.insert(0, n.name)
      n = n.parent
    return "/".join(path)
  def print_children(self):
    for c in self.children:
      if c.is_dir:
        print(f"dir {c.name}")
      else:
        print(f"{c.size} {c.name}")
  def is_child(self, name):
    for c in self.children:
      if c.name == name:
        return c
      else:
        return None


def main() -> None:

  """Read the lines from the data file"""
  with open('example.txt') as f:
    lines = [x.strip() for x in f.readlines()]

  root = Node(name='/', is_dir=True, is_root=True)
  cur_dir = root
  for l in lines:
    if l[0] == '$':
      if l[2:4] == 'cd':
        dir = l.split()[2]
        if dir == '/':
          cur_dir = root
        elif dir == '..':
          cur_dir = cur_dir.parent
        else:
          check = cur_dir.is_child(dir)
          if check is not None:
            cur_dir = check
          else:
            n = Node(name=dir, is_dir=True, is_root=False)
            n.set_parent(cur_dir)
            cur_dir = n
    elif l[0:3] == 'dir':
      dir_name = l.split()[1]
      n = Node(name=dir_name, is_dir=True, is_root=False)
      cur_dir.add_child(n)
    elif l[0] in string.digits:
      file_name = l.split()[1]
      file_size = l.split()[0]
      n = Node(name=file_name, is_dir=False, is_root=False, size=int(file_size))
      cur_dir.add_child(n)

  print(root.print_children())

main()
