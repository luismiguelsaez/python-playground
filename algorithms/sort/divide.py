from random import randrange

def split_list(l:list):
  l1 = l[:len(l)//2]
  l2 = l[len(l)//2:]

  return l1, l2

def sort_bubble(l: list)->list:

  for i in reversed(range(len(l))):
    for j in range(0,i):
      if l[j] > l[j+1]:
        l[j], l[j+1] = l[j+1], l[j]

  return l

def merge_lists(l1:list, l2:list)->list:

  merged_list = []

  idx1 = 0
  idx2 = 0
  while idx1 < len(l1) and idx2 < len(l2):
    if l1[idx1] < l2[idx2]:
      merged_list.append(l1[idx1])
      idx1 += 1
    elif l1[idx1] > l2[idx2]:
      merged_list.append(l2[idx2])
      idx2 += 1
    else:
      merged_list.append(l1[idx1])
      merged_list.append(l2[idx2])
      idx1 += 1
      idx2 += 1

  if idx1 == len(l1):
    #merged_list = merged_list + l2[idx2:]
    merged_list = [*merged_list, *l2[idx2:]] 
  elif idx2 == len(l2):
    #merged_list = merged_list + l1[idx1:]
    merged_list = [*merged_list, *l1[idx1:]]

  return merged_list


if __name__ == "__main__":
  test_list = [randrange(10) for x in range(20)]
  
  # Split method
  test_list1, test_list2 = split_list(test_list)

  print("Merging lists:", sort_bubble(test_list1), sort_bubble(test_list2))

  merged_list = merge_lists(test_list1, test_list2)
  merged_list_len = len(merged_list)
  print("Merged lists (1):", merged_list)

  # Normal method
  print("Merged lists (2):", sort_bubble(test_list))
