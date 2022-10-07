

def merge_lists(list1: list,list2: list)->list:
	
    count1 = 0
    count2 = 0
    merged = []

    while count1 < len(list1) and count2 < len(list2):
     
      if list1[count1] < list2[count2]:
          merged.append(list1[count1])
          count1 += 1
      elif list2[count2] < list1[count1]:
          merged.append(list2[count2])
          count2 += 1
      else:
          merged.append(list2[count2])
          count1 += 1
          count2 += 1

    if count1 < len(list1):
      for i in list1[count1:]:
        merged.append(i)
    elif count2 < len(list2):
      for i in list2[count2:]:
        merged.append(i)

    return merged


if __name__ == "__main__":

    list1 = [0,2,5,7,9,11,21] 
    list2 = [1,3,4,8,12,33,24,56] 

    print(merge_lists(list1,list2))

