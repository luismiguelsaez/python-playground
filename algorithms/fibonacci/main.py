
def fib(n: int, memo: dict = {}) -> int:
  if n <= 2:
    return 1
  else:
    if n in memo:
      return memo[n]
    else:
      memo[n] = fib(n-1, memo) + fib(n-2, memo)
      return memo[n]

print(fib(55))
