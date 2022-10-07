
def sort_bubble(list: list)->list:

  for i in reversed(range(len(list))):
    j = 0
    while j < i:
      if list[j] > list[j+1]:
        buff = list[j]
        list[j] = list[j+1]
        list[j+1] = buff
      j += 1

  return list

if __name__ == "__main__":

  test_list = [7,8,2,3,6,5,1,4]

  print(sort_bubble(test_list))
