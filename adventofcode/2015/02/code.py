
wrapping_paper = 0
ribbon = 0
for line in [x.strip() for x in open('input.txt').readlines()]:
  l, w, h = line.split('x')
  surface = int(l)*int(w)*2 + int(l)*int(h)*2 + int(h)*int(w)*2
  smallest = min(int(l)*int(w), int(l)*int(h), int(h)*int(w))
  wrapping_paper += surface + smallest

  smallest_sides = sorted([int(l), int(w), int(h)])
  ribbon = ( smallest_sides[0]*2 + smallest_sides[1]*2 ) + ( int(l)*int(w)*int(h) )

  print(f"Ribbon",smallest_sides, ( smallest_sides[0]*2 + smallest_sides[1]*2 ) + ( int(l)*int(w)*int(h) ))

print(f"Part 1: {wrapping_paper}")
# Result: 1588178

print(f"Part 2: {ribbon}")
# Result:
