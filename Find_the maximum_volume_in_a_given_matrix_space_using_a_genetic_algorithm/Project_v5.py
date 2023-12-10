# 1.문제 정의

import numpy as np
import pandas as pd
from time import perf_counter

# 데이터 불러오기
data = pd.read_csv('C:\\Users\\win\\Desktop\\kgh\\Algorithm_Project\\input.csv')
vectors = data.iloc[0:20].to_numpy()  # 첫 행은 인덱스, 나머지가 벡터 값

# 초기 설정
num_vectors = 20    # 행렬의 행 수
population_size = 100  # 인구 크기
vector_length = 10000  # 전체 벡터의 수 설정 (예시로 10000으로 가정)
num_generations = 100  # 세대 수
mutation_rate = 0.1   # 돌연변이율
# print(vectors.shape)

# 2. 초기 인구 생성


def initialize_population(pop_size, num_vectors):
    # 각 행렬의 열이 중복되지 않도록 선택
    population = []
    for _ in range(pop_size):
        x_indices = np.random.choice(num_vectors, 2, replace=False)
        if x_indices[0]>x_indices[1]:
          x_indices[0], x_indices[1] = x_indices[1], x_indices[0]
        y_indices = np.random.choice(vector_length, 2, replace=False)
        if y_indices[0]>y_indices[1]:
          y_indices[0], y_indices[1] = y_indices[1], y_indices[0]
        indices = np.stack((x_indices, y_indices), axis=-1)
        population.append(indices)
    return np.array(population)

# x와 y 좌표를 결합하여 2차원 인덱스 생성
# population = initialize_population(population_size, num_vectors)
# # print(population)
# population = population.reshape(100,4).tolist()

# # print(population)

# 3. 적합도 함수 정의


def fitness(matrix):
    matrix_product = np.dot(matrix, matrix.transpose())
    matrix_det = np.linalg.det(matrix_product)
    if np.abs(matrix_det) < 1e-5:  # 행렬식이 매우 작은 경우 낮은 적합도 반환
        return 0
    volume = np.sqrt(np.abs(matrix_det))
    return volume

# print(fitness(vectors))

def evaluate_population(population):
    fitness_scores = []
    # population (100, 100, 20, 2) 100개의 개체군이 각각(100x20) 행렬로 이루어져 있으며,
    # 각 개체군의 요소는 vectors의 index [x, y]쌍으로 가지고 있다.
    for individual in population:
        # print("individual: ", individual)

        # 각 개체군을 가져옴. mtx.shape = (100, 20, 20)
        # 각 개체의 인덱스를 사용하여 vectors에서 실제 값을 가져와 행렬을 생성
        matrix = np.array(vectors[individual[0]:individual[2], individual[1]:individual[3]])
        # print(matrix.shape)

        # Volume 계산 결과와 indexing한 좌표를 저장함.
        fitness_scores.append([fitness(matrix), individual])
    # print(fitness_scores)
    return fitness_scores



# fitness_scores = evaluate_population(population)
# print(len(fitness_scores))
# print(fitness_scores.shape)
# print(*fitness_scores, sep = '\n')



# 4. 선택
def select_parents(fitness_scores):
    # 적합도 점수만 추출
    scores = [score[0] for score in fitness_scores]

    # 총 적합도 점수 계산
    total_fitness = sum(scores)

    # 각 개체의 선택 확률 계산
    probabilities = [score / total_fitness for score in scores]

    # 선택 확률에 따라 부모를 무작위로 선택
    selected_indices = np.random.choice(len(fitness_scores), size=len(fitness_scores), replace=True, p=probabilities)

    # 선택된 인덱스를 기반으로 부모 선택
    parents = [fitness_scores[index] for index in selected_indices]
    return parents

# # 적합도 점수를 바탕으로 부모 선택
# parents = select_parents(fitness_scores)

# 선택된 부모 출력
# print(parents.shape)
# print(parents)

# 5. 교차

# 5. 교차
def crossover(parents):
    offspring = []
    num_parents = len(parents)

    for i in range(0, num_parents - 1, 2):
        # 부모 개체 선택
        parent1 = parents[i][1]
        parent2 = parents[i + 1][1]

        # 교차 위치 선택 (부모 배열의 길이에 따라 조정)
        cut = np.random.randint(1, len(parent1) - 1)

        # 자손 생성
        child1 = np.concatenate([parent1[:cut], parent2[cut:]])
        child2 = np.concatenate([parent2[:cut], parent1[cut:]])

        offspring.extend([child1, child2])

    # 부모 배열의 길이가 홀수인 경우 마지막 부모 처리
    if num_parents % 2 != 0:
        offspring.append(parents[-1][1])

    return np.array(offspring)

# # 교차 함수 호출 및 자손 출력
# offspring = crossover(parents)
# print(offspring)

# 6. 돌연변이

# 6. 돌연변이
def mutation(offspring_crossover, mutation_rate, num_vectors, vector_length):
    for idx in range(offspring_crossover.shape[0]):
        if np.random.rand() < mutation_rate:
            # 돌연변이가 발생할 유전자 위치 선택
            gene_idx = np.random.randint(4)  # 0에서 3 사이의 정수 (x1, y1, x2, y2 중 하나)

            # 돌연변이 적용
            if gene_idx % 2 == 0:  # x1 또는 x2의 경우
                random_value = np.random.randint(num_vectors)
            else:  # y1 또는 y2의 경우
                random_value = np.random.randint(vector_length)

            # 돌연변이 적용
            offspring_crossover[idx, gene_idx] = random_value
    return offspring_crossover

# # 돌연변이 함수 호출
# mutated_offspring = mutation(offspring, mutation_rate, num_vectors, vector_length)


# print(mutated_offspring)

# 7-9. 새로운 세대 생성 및 종료 조건 검사 및 결과 추출
#실제 실행 부분

start = perf_counter()
# 개체(인구) 생성
population = initialize_population(population_size, num_vectors)
# print(population)
population = population.reshape(100,4).tolist()
fitness_scores = evaluate_population(population)
# 적합도 점수를 바탕으로 부모 선택
parents = select_parents(fitness_scores)
# 교차 함수 호출 및 자손 출력
offspring = crossover(parents)
# # 돌연변이 함수 호출
# mutated_offspring = mutation(offspring, mutation_rate, num_vectors, vector_length)

best_fitness = 0
best_index   = []
fitness_threshold = 3.9471414633881875e+34  # 최대 적합도 종료 임계값
# num_generations = 100
for generation in range(num_generations):
    # 돌연변이 함수 호출
    mutated_offspring = mutation(offspring, mutation_rate, num_vectors, vector_length)  
    # 적합도 평가
    fitness_scores = evaluate_population(mutated_offspring)

    # 이번 세대의 최대 적합도와 해당하는 개체의 인덱스 찾기
    max_fitness_this_generation = 0
    max_fitness_index = 0
    for i, score in enumerate(fitness_scores):
        if score[0] > max_fitness_this_generation:
            max_fitness_this_generation = score[0]
            max_fitness_index = i

    # 최대 적합도가 이전 최고값을 초과하는 경우 업데이트
    if max_fitness_this_generation > best_fitness:
        best_fitness = max_fitness_this_generation
        best_index = fitness_scores[max_fitness_index][1]  # [x1, y1, x2, y2] 정보 저장

    # 종료 조건 검사: 최대 적합도가 임계값 이상인 경우
    if best_fitness >= fitness_threshold:
        print(f"Generation {generation}: 최대 적합도가 {fitness_threshold} 이상이므로 종료합니다.")
        break

    # 부모 선택
    parents = select_parents(fitness_scores)  # 여기서 population 인자 제거

    # 교차
    offspring = crossover(parents)  # 여기서 두 번째 인자 제거

    # 돌연변이 적용
    mutated_offspring = mutation(offspring, mutation_rate, num_vectors, vector_length)

    # 새로운 개체군 생성
    population = mutated_offspring
end = perf_counter()




# 9. 결과 추출

print(f"최대 적합도 = {best_fitness}, vectors의 인덱스 = {best_index}, 실행 시간 = {(end-start)* 1e6:.5f}us")
print("최대 적합도 행렬")
print(vectors[best_index[0]:best_index[2], best_index[1]:best_index[3]])