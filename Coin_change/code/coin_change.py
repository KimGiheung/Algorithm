# 액면
d = [16,10,5,1]
# 거스름돈
n = 20

C = [float('inf')]*(n+1)
print(C)
C[0] = 0

for i in range(1, n+1):
    for j in d:
        if j<=i and (C[i-j] + 1 < C[i]):
            C[i] = C[i-j]+1

print(C)
