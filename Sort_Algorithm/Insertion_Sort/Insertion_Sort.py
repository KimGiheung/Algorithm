import numpy as np

A = np.random.randint(1, 100, size=(1000))

for i in range(1, len(A)):
    CurrentElement = A[i]
    j = i-1
    while j>=0 and A[j]>CurrentElement:
        A[j+1] = A[j]
        j -= 1
    A[j+1] = CurrentElement
print(A)