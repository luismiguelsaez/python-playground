def split_text(text: str, length: int)->list:
  strings = []
  for i in range(len(text)):
    strings.append(text[i:i+length])

  return list(filter(lambda x: len(x) == length, strings))


def find_in_text(text: str, sub: str, case=True)->bool:

  if not case:
    sub = sub.lower()
    text = text.lower()

  if sub in split_text(text, len(sub)):
    return True
  else:
    return False


def main():

  test_text = "Hotel transilvania"
  test_subs = "Trans"

  if find_in_text(test_text, test_subs, case=False):
    print("Found substring '{}' in text '{}'".format(test_subs, test_text))
  else:
    print("KO")


main()
