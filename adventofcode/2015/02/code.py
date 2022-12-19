
wrapping_paper = 0
for line in [x.strip() for x in open('input.txt').readlines()]:
  l, w, h = line.split('x')
  surface = int(l)*int(w)*2 + int(l)*int(h)*2 + int(h)*int(w)*2
  smallest = min(int(l)*int(w), int(l)*int(h), int(h)*int(w))
  total = surface + smallest
  print(l, w, h, surface, smallest)
  wrapping_paper += total

print(f"Part 1: {wrapping_paper}")
# Result: 1588178
