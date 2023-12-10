# -*- coding: utf-8 -*-
"""Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pdX3Oz8BBdKQfcSlRd4NVYzqh3_Hgh_J

# 1.문제 정의
"""

import numpy as np
import pandas as pd

# 데이터 불러오기
data = pd.read_csv('/content/drive/MyDrive/2023-2알고리즘/[Project] 주어진 행렬 공간 중에서 최대 volume 구하기/input.csv')
vectors = data.iloc[1:21].to_numpy()  # 첫 행은 인덱스, 나머지가 벡터 값

# 초기 설정
num_vectors = 20    # 행렬의 행 수
population_size = 100  # 인구 크기
vector_length = 10000  # 전체 벡터의 수 설정 (예시로 10000으로 가정)
num_generations = 100  # 세대 수
mutation_rate = 0.1   # 돌연변이율
print(vectors)

"""# 2. 초기 인구 생성

"""

def initialize_population(pop_size, num_vectors):
    # x 좌표를 0부터 19 사이에서 선택
    x_indices = np.random.randint(0, num_vectors, size=(pop_size, num_vectors)) # num_vectors-1 대신 num_vectors 사용

    # y 좌표를 0부터 9999 사이에서 선택
    y_indices = np.random.randint(0, vector_length-1, size=(pop_size, num_vectors))

    # x와 y 좌표를 결합하여 2차원 인덱스 생성
    indices = np.stack((x_indices, y_indices), axis=-1)

    return indices

# x와 y 좌표를 결합하여 2차원 인덱스 생성
population = initialize_population(population_size, num_vectors)

for _ in range(99):
    population = np.concatenate((population, initialize_population(population_size, num_vectors)), axis=0)
population = population.reshape(100,100,20,2)
print("population size: ", population.shape)
print(population)

"""# 3. 적합도 함수 정의

"""
def fitness(matrix):
    matrix_product = np.dot(matrix, matrix.transpose())
    return np.sqrt(np.abs(np.linalg.det(matrix_product))) # sqrt(|det(A^T * A)|)

def evaluate_population(vectors):
    fitness_scores = []
    matrix = []
    for mtx in population:
      for individual in mtx:
        # 각 개체의 인덱스를 사용하여 vectors에서 실제 값을 가져와 행렬을 생성
        matrix.append([vectors[x, y] for x, y in individual])
      matrix = np.array(matrix)
      print(matrix.shape)
      fitness_scores.append(fitness(matrix))
    return np.array(fitness_scores)



fitness_scores = evaluate_population(vectors)
print(fitness_scores.shape)


"""# 4. 선택"""

def select_parents(population, fitness_scores):
    probabilities = fitness_scores / fitness_scores.sum()
    selected_indices = np.random.choice(len(population), size=len(population), replace=True, p=probabilities)
    return population[selected_indices]

parents = select_parents(population, fitness_scores)

"""# 5. 교차"""

def crossover(parents):
    offspring = []
    for i in range(0, len(parents), 2):
        parent1 = parents[i]
        parent2 = parents[i + 1]
        cut = np.random.randint(1, len(parent1)-1)
        child1 = np.concatenate([parent1[:cut], parent2[cut:]])
        child2 = np.concatenate([parent2[:cut], parent1[cut:]])
        offspring.extend([child1, child2])
    return np.array(offspring)

offspring = crossover(parents)

"""# 6. 돌연변이"""

# 돌연변이 함수
def mutation(offspring_crossover, mutation_rate, num_vectors):
    for idx in range(offspring_crossover.shape[0]):
        if np.random.rand() < mutation_rate:
            random_index = np.random.randint(offspring_crossover.shape[1])
            random_value = np.random.randint(num_vectors)
            offspring_crossover[idx, random_index] = random_value
    return offspring_crossover
# 돌연변이 함수 호출
num_vectors = 10000  # 전체 벡터의 수 설정
mutated_offspring = mutation(offspring, mutation_rate, num_vectors)

"""# 7-8. 새로운 세대 생성 및 종료 조건 검사"""

for generation in range(num_generations):
    fitness_scores = evaluate_population(population, vectors)
    parents = select_parents(population, fitness_scores)
    offspring = crossover(parents)  # 여기서 두 번째 인자 제거
    mutated_offspring = mutation(offspring, mutation_rate, num_vectors)
    population = mutated_offspring
    # 종료 조건 검사
    # ...

"""# 9. 결과 추출"""

final_fitness = evaluate_population(population, vectors)
best_index = np.argmax(final_fitness)
best_solution = population[best_index]
best_volume = final_fitness[best_index]

print("최대 볼륨:", best_volume)
print("해당 벡터의 인덱스:", best_solution)

