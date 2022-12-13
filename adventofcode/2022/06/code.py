
with open('input.txt') as file:
  msg = file.read()

def get_marker(window: int, msg: str)->int:
  for i in range(len(msg)-window+1):
    slice = msg[i:i+window]
    if len(set(slice)) == window:
      processed_chars = i+window
      return processed_chars
  return -1

part_1 = get_marker(4, msg)
print(f"Part 1 - Processed chars: {part_1}")

part_2 = get_marker(14, msg)
print(f"Part 2 - Processed chars: {part_2}")
