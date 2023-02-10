import string
import random

a = "".join(random.choices(string.digits + string.ascii_letters, k=20))
print(a)
