
def fib(n: int, memo: dict = {}) -> int:
  if n <= 2: return 1
  if n in memo: return memo[n]

  memo[n] = fib(n-1, memo) + fib(n-2, memo)
  return memo[n]

for i in range(1,20):
  print(fib(i))
