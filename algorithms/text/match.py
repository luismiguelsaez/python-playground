def split_text(text: str, length: int)->list:
  strings = []
  for i in range(len(text)):
    strings.append(text[i:i+length])

  return list(filter(lambda x: len(x) == length, strings))


def find_in_text(text: str, sub: str, case=False)->bool:

  if not case:
    sub = sub.lower()
    text = text.lower()

  if sub in split_text(text, len(sub)):
    return True
  else:
    return False


def keyboard_detect_error(k: str)->list:

  keys = [
    "QWERTYUIOP",
    "ASDFGHJKL",
    "ZXCVBNM"
  ]

  keys_group = []
  for i in range(len(keys)):
    for j in range(len(keys[i])):
      if keys[i][j] == k:
        keys_group += keys[i][j:j+2]
        keys_group += keys[i][j-1:j]

  return keys_group


def main():

  hotel_names = [
    "Grand Transilvania",
    "Obscure Castle of Illusion",
    "Hollow Casquet of Hell"
  ]

  test_subs = "castle"

  for hotel_name in hotel_names:
    if find_in_text(hotel_name, test_subs):
      print("Found substring '{}' in text '{}'".format(test_subs, hotel_name))

  print(keyboard_detect_error("G"))

main()
