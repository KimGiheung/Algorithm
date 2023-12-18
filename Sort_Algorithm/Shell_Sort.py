import numpy as np

A = np.random.randint(1, 100, size=(1000))

h = [20, 10, 5, 1]

for i in h:
    for j in range(i, len(A)):
        CurrentElement = A[j]
        while j>=i and A[j-i]>CurrentElement:
            A[j] = A[j-i]
            j -= i
        A[j] = CurrentElement


print(A)