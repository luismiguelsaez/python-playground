
def sort_bubble(list: list)->list:

  for i in reversed(range(len(list))):
    for j in range(0,i):
      if list[j] > list[j+1]:
        buff = list[j]
        list[j] = list[j+1]
        list[j+1] = buff

  return list

if __name__ == "__main__":

  test_list = [7,8,2,3,6,5,1,4]

  print(sort_bubble(test_list))
