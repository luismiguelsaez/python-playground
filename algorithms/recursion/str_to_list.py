
def str_to_list(s):
  def inner(i):
    while True:
      next_item = next(i)
      if next_item == '[':
        yield [x for x in str_to_list(i)]
      elif next_item == ']':
        return
      elif next_item == ',':
        pass
      else:
        yield int(next_item)
  return inner(iter(s))


lst = str_to_list('[1,2,3,4,[5,6],8]')



for i in list(next(lst)):
  print(i)
