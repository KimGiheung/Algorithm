import numpy as np
import random

# 점들 정의
points = {
    'A': (0, 3), 'B': (7, 5), 'C': (6, 0), 'D': (4, 3),
    'E': (1, 0), 'F': (5, 3), 'H': (4, 1), 'G': (2, 2)
}

#==========================+
#      함수 정의 부분       |
#==========================+
# 두 점 사이의 거리 계산 함수
def calculate_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

# 경로의 총 거리 계산 함수
def total_distance(path):
    distance = 0
    for i in range(len(path)):
        distance += calculate_distance(points[path[i]], points[path[(i + 1) % len(path)]])
    return distance

# 적합도 함수 (경로 거리의 역수)
def fitness(path):
    return 1 / total_distance(path)

# 토너먼트 선택 함수
def tournament_selection(population, tournament_size):
    selected = random.sample(population, tournament_size)
    selected.sort(key=lambda x: fitness(x), reverse=True)
    return selected[0]

# 사이클 교차 함수
def cycle_crossover_optimized(parent1, parent2):
    child = [None] * len(parent1)
    cycle_elements = set()
    index = 0
    while None in child:
        
        # print(f"parent1[{index}]: {parent1[index]}")

        if parent1[index] not in cycle_elements:
            cycle_elements.add(parent1[index])
            child[index] = parent1[index]
            index = parent1.index(parent2[index])
        else:
            for i, gene in enumerate(child):
                if gene is None:
                    child[i] = parent2[i]
                    cycle_elements.add(parent2[i])
            break
    return child

# 변이 함수 (스왑 변이)
def mutate(path, mutation_rate):
    mutated_path = path.copy()
    for i in range(len(mutated_path)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(mutated_path) - 1)
            mutated_path[i], mutated_path[j] = mutated_path[j], mutated_path[i]
    return mutated_path

# 인구 초기화 함수
def initialize_population(size, points):
    population = []
    for _ in range(size):
        path = list(points.keys())
        random.shuffle(path)
        population.append(path)
    return population
#======================================================

#==========================+
#    알고리즘 실행 부분     |
#==========================+
# 매개변수 설정
population_size = 8
num_generations = 100
crossover_rate = 1.0
mutation_rate = 0.01

# 첫 번째 인구 초기화
population = initialize_population(population_size, points)

# 유전 알고리즘 메인 루프
best_solution = None
best_fitness = 0
for generation in range(num_generations):
    new_population = []
    for _ in range(len(population)):
        # 선택
        parent1 = tournament_selection(population, 3)
        parent2 = tournament_selection(population, 3)

        # 교차
        if random.random() < crossover_rate:
            child = cycle_crossover_optimized(parent1, parent2)
        else:
            child = parent1

        # 변이
        child = mutate(child, mutation_rate)
        # print(child)
        # print("mutation_rate: ", mutation_rate)
        new_population.append(child)
        # print(new_population)

        # 최적 해결책 업데이트
        child_fitness = fitness(child)
        if child_fitness > best_fitness:
            best_solution = child
            best_fitness = child_fitness

    population = new_population

# 최적 경로와 총 거리 출력
print("Best Path:", best_solution)
print("Total Distance:", total_distance(best_solution))


