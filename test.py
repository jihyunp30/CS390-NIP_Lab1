import numpy as np

a = np.random.randint(100, size = (10, 10))
print(a)
b = (a.max(axis=1)[:, None])
print(b)
a[a < b] = 0
print(a)