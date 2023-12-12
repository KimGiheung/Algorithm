import random
import numpy as np

# 좌표 정의
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
        distance += np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

# 초기 인구 생성
def create_initial_population(size, points):
    population = []
    for _ in range(size):
        path = points.copy()
        random.shuffle(path)
        population.append(path)
    return population

# 적합도 계산
def fitness(path):
    return 1 / calculate_distance(path)

# 선택
def select(population, fitnesses, num_parents):
    selected = np.random.choice(population, size=num_parents, replace=False, p=fitnesses / fitnesses.sum())
    return selected

# 교차 (사이클 교차)
def crossover(parent1, parent2):
    child = parent1.copy()
    # 사이클 교차 구현
    # ...
    return child

# 돌연변이
def mutate(path, mutation_rate):
    for i in range(len(path)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(path) - 1)
            path[i], path[j] = path[j], path[i]
    return path

# 유전 알고리즘 실행
def genetic_algorithm(coordinates, population_size=8, num_generations=100, mutation_rate=0.01):
    points = list(coordinates.keys())
    population = create_initial_population(population_size, points)

    for generation in range(num_generations):
        fitnesses = np.array([fitness(path) for path in population])
        selected = select(population, fitnesses, len(population) // 2)

        # 다음 세대 생성
        next_generation = []
        while len(next_generation) < population_size:
            parents = np.random.choice(selected, size=2, replace=False)
            child = crossover(parents[0], parents[1])
            child = mutate(child, mutation_rate)
            next_generation.append(child)

        population = next_generation

    # 최적 경로 반환
    best_path = max(population, key=fitness)
    return best_path, calculate_distance(best_path)
#======================================================

#==========================+
#    알고리즘 실행 부분     |
#==========================+
# 알고리즘 실행
best_path, distance = genetic_algorithm(coordinates)
print("최적 경로:", best_path)
print("이동 거리:", distance)
