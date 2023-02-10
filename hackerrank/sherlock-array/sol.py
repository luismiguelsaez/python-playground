def balancedSums(arr):

    if len(arr) % 2 == 0:
      ini = len(arr)//2-1
    else:
      ini = len(arr)//2

    print(f"Starting at position {ini}/{len(arr)}")
    for i in range(ini, -1, -1):
        left = sum(arr[:i])
        right = sum(arr[len(arr)-i:])

        left2 = sum(arr[:len(arr)-i])
        right2 = sum(arr[i:])

        if left == right or left2 == right2:
            return 'YES'
        
    return 'NO'

def main():
  with open('case-3.txt') as f:
    c = 1
    cases = 1
    num_cases = 0
    for l in [x.strip() for x in f.readlines()]:
      if c == 1:
        num_cases = l
      elif c % 2 == 0:
        print(f"Case {cases} has {l} elements")
        cases += 1
      else:
        print(balancedSums([int(x) for x in l.split(' ')]))
      c += 1

main()
