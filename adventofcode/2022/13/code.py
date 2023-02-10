

def str_to_list(string: str):
  def inner(item):
    while True:
      next_item = next(item)
      if next_item == '[':
        yield [x for x in inner(item)]
      elif next_item == ']':
        return
      elif next_item == ',':
        pass
      else:
        yield int(next_item)
  return list(next(inner(iter(string))))


def compare(left, right):
  if len(left) == len(right):
    for i in range(len(left)):
      if isinstance(left[i], int) and isinstance(right[i], int):
        if left[i] > right[i]:
          return False
      elif isinstance(left[i], list) and isinstance(right[i], int):
        if not compare(left[i], [right[i]]):
          return False
      elif isinstance(left[i], int) and isinstance(right[i], list):
        if not compare([left[i]], right[i]):
          return False
    return True
  elif len(left) < len(right):
    return True
  else:
    return False


def main():
  packets = [i.strip() for i in open('example_1.txt').readlines() if i != '\n']
  pairs = [(packets[i], packets[i+1]) for i in range(0, len(packets), 2)]

  sum = 0
  for idx, pair in enumerate(pairs):
    left, right = str_to_list(pair[0]), str_to_list(pair[1])
    if compare(left, right):
      sum += idx+1

  print(f"Part 1: {sum}")


main()
