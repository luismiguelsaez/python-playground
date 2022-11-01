import time

def sort_bubble(list: list)->list:

  for i in reversed(range(len(list))):
    for j in range(0,i):
      if list[j] > list[j+1]:
        list[j], list[j+1] = list[j+1], list[j]

  return list

def sort_bubble_alt(list: list)->list:
  
  last = len(list)
  while last > 0:
    for i in range(last-1):
        if list[i] > list[i+1]:
            list[i], list[i+1] = list[i+1], list[i]
    last -= 1

  return list

def find_split(list: list,num: int)->list[list]:

  if len(list) % 2 != 0:
    mid_idx = int((len(list)-1)/2)
    if list[mid_idx] == num:
      return mid_idx
    else:
      return [list[0:mid_idx],list[mid_idx+1:len(list)]]
  else:
    return [list[0:int(len(list)/2)],list[int(len(list)/2):len(list)]]

if __name__ == "__main__":

  test_list = [1,8,4,3,2,7,6,5]

  sorted = sort_bubble(test_list)
  print(sorted)