import numpy as np
n = 4#개
C = 10#kg


wi = [5, 4, 6, 3]
vi = [10, 40, 30, 50]
K = np.full((n+1, C+1), float('inf'))
# print(C)

for i in range(n+1):
    K[i,0] = 0
for w in range(C+1):
    K[0,w] = 0

for i in range(1,n+1):
    for w in range(1,C+1):
        if wi[i-1] > w:
            K[i,w] = K[i-1,w]       # i번째 물건을 배낭에 넣었을 때 임시 배낭 무게를 초과하면 넣지 않음/
                                    # == 배낭 가치가 직전 물건을 알고리즘 돌렸을 때와 변하지 않는다. => K[i,w] = K[i-1,w]
        else:
            K[i,w] = max(K[i-1,w], K[i-1,w-wi[i-1]] + vi[i-1])


print(K)

