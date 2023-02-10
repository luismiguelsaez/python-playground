
class Node:
  def __init__(self, value, next = None):
    self.value = value
    self.next = next
  
  def set_next(self, n):
    self.next = n

def print_list(head: Node)->None:
  current = head
  print(current.value)
  while current.next != None:
    current = current.next
    print(current.value)

def insert_node(head: Node, after: int, value: int):
  current = head
  while current.next != None:
    if current.value == after:
      n = Node(value, current.next)
      current.set_next(n)
      return True
    current = current.next
  return False

def main():

  head = Node(0)
  current = head
  for i in range(1, 10):
    n = Node(i, None)
    current.set_next(n)
    current = n

  insert_node(head, 8, 100)
  print_list(head)

main()
