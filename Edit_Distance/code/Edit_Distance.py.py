import numpy as np
S = 'strong'
T = 'stone'

s_len = len(S)
t_len = len(T)

C = np.full((s_len+1, t_len+1), float('inf'))
# print(C)

C[0,0] = 0

for i in range(1,s_len+1):
    C[i][0] = i
for j in range(1,t_len+1):
    C[0][j] = j

for i in range(1,s_len+1):
    for j in range(1,t_len+1):
        if S[i-1] == T[j-1]:
            C[i][j] = min(C[i-1,j]+1, C[i,j-1]+1, C[i-1,j-1])
        else:
            C[i][j] = min(C[i-1,j]+1, C[i,j-1]+1, C[i-1,j-1]+1)


print(C)
print(f'최소 편집 거리: {int(C[s_len, t_len])}')
