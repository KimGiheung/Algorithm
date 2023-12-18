import numpy as np

A = np.random.randint(1,100,size=(1000))

for i in range(len(A)-1):
    min = i
    for j in range(i+1, len(A)):
        if A[min]>A[j]:
            min = j
    A[min],A[i] = A[i], A[min]

print(A)