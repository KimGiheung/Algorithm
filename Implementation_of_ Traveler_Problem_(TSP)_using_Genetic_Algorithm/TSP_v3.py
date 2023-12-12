import numpy as np
import random

# 좌표 설정
coordinates = {
    'A': (0, 3), 'B': (7, 5), 'C': (6, 0), 'D': (4, 3),
    'E': (1, 0), 'F': (5, 3), 'G': (2, 2), 'H': (4, 1)
}
#==========================+
#      함수 정의 부분       |
#==========================+
# 거리 계산 함수
def calculate_distance(path):
    distance = 0
    for i in range(len(path)):
        (x1, y1), (x2, y2) = coordinates[path[i]], coordinates[path[(i + 1) % len(path)]]
        distance += np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance

# 적합도 함수
def fitness(path):
    return 1 / calculate_distance(path)

# 초기 인구 생성
def create_initial_population(size, points):
    return [random.sample(points, len(points)) for _ in range(size)]

# 룰렛 휠 선택
def roulette_wheel_selection(population, fitnesses, num_parents):
    total_fitness = sum(fitnesses)
    selection_probs = [f / total_fitness for f in fitnesses]
    selected_indices = np.random.choice(range(len(population)), size=num_parents, replace=False, p=selection_probs)
    return [population[i] for i in selected_indices]

# 사이클 교차 연산
def cycle_crossover(parent1, parent2):
    child = parent1.copy()
    index = 0
    while True:
        child[index] = parent2[index]
        index = parent1.index(parent2[index])
        if index == 0:
            break
    return child

# 돌연변이
def mutate(path, mutation_rate):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(path)), 2)
        path[i], path[j] = path[j], path[i]
    return path

# 유전 알고리즘
def genetic_algorithm(coordinates, population_size=8, num_generations=100, mutation_rate=0.01):
    points = list(coordinates.keys())
    population = create_initial_population(population_size, points)
    best_path = None
    best_distance = float('inf')

    for generation in range(num_generations):
        fitnesses = [fitness(path) for path in population]
        selected = roulette_wheel_selection(population, fitnesses, len(population) // 2)

        next_generation = []
        while len(next_generation) < population_size:
            parents_indices = np.random.choice(len(selected), size=2, replace=False)
            parents = [selected[i] for i in parents_indices]
            child = cycle_crossover(parents[0], parents[1])
            child = mutate(child, mutation_rate)
            next_generation.append(child)

        population = next_generation

        # 최적 경로 업데이트
        for path in population:
            distance = calculate_distance(path)
            if distance < best_distance:
                best_path, best_distance = path, distance

    return best_path, best_distance
#======================================================

#==========================+
#    알고리즘 실행 부분     |
#==========================+
# 유전 알고리즘 실행
best_path, distance = genetic_algorithm(coordinates)
print("최적 경로:", best_path)
print("이동 거리:", distance)
