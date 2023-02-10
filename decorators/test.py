from random import randrange
from time import perf_counter

def timer(f):
  def wrapper(*args, **kwargs):
    print("Begin")
    t_start = perf_counter()
    val = f(*args, **kwargs)
    t_stop = perf_counter()
    print(f"End: {t_stop - t_start}")
    return val

  return wrapper

@timer
def randomize(r: int, n: int):
  [randrange(r) for _ in range(n)]

def main():
  randomize(100, 10_000_000)

main()
