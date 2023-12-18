import numpy as np

A = np.random.randint(1,100,size=(1000))

for i in range(len(A)):
    for j in range(1, len(A)-i):
        if A[j]<A[j-1]:
            A[j-1], A[j] = A[j], A[j-1]

print(A)

