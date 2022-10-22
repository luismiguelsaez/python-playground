def sort_dict_by_key(dictionary:dict)->dict:
  sorted_dict = dict(sorted(dictionary.items()))
  return sorted_dict

def sort_dict_by_value(dictionary:dict)->dict:
  sorted_dict = dict(sorted(dictionary.items(),key=lambda item: item[1]))
  return sorted_dict

def print_dict(dictionary:dict):
  for key,value in dictionary.items():
    print("{} -> {}".format(key,value))

def main():
  test_dict = {
    "Brian": 10,
    "Karen": 2,
    "John": 1
  }

  print_dict(sort_dict_by_key(test_dict))
  print_dict(sort_dict_by_value(test_dict))


if __name__ == "__main__":
  main()