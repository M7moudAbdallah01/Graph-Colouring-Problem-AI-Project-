import random
import time

POPULATION_SIZE = 20
MAX_GENERATIONS = 100
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.8
RETRIES = 5

# Initialize Population
def initialize_population(num_nodes, k, population_size):
    population = []
    for i in range(population_size):
        chromosome = create_chromosome(num_nodes, k)
        population.append(chromosome)
    return population

def create_chromosome(num_nodes, k):
    chromosome = []
    for i in range(num_nodes):
        color = random.randint(0, k - 1)
        chromosome.append(color)
    return chromosome

# calculate_conflicts
def calculate_conflicts(chromosome, edges):
    conflicts = 0
    for u, v in edges:
        if chromosome[u] == chromosome[v]:
            conflicts += 1
    return conflicts

# Selection
def tournament_selection(population, scores, tournament_size=3):
    selected = random.sample(range(len(population)), tournament_size)
    best_index = selected[0]
    for i in selected:
        if scores[i] < scores[best_index]:
            best_index = i
    return population[best_index][:]

# crossover function
def crossover(parent1, parent2, rate):
    if len(parent1) < 2 or random.random() > rate:
        return parent1[:], parent2[:]
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2


# mutate function
def mutate(chromosome, k, rate):
    if k < 2:
        return chromosome
    for i in range(len(chromosome)):
        if random.random() < rate:
            options = [c for c in range(k) if c != chromosome[i]]
            chromosome[i] = random.choice(options)
    return chromosome


# next_generation function
def next_generation(population, scores, best, k, pop_size,mutation_rate, crossover_rate, select):
    new_population = [best[:]]
    while len(new_population) < pop_size:
        p1 = select(population, scores)
        p2 = select(population, scores)
        for child in crossover(p1, p2, crossover_rate):
            mutate(child, k, mutation_rate)
            new_population.append(child)
    return new_population[:pop_size]

# Genetic Algorithm M
def run_genetic_algorithm(num_nodes, edges, k, population_size,max_generations, mutation_rate,crossover_rate):
    population = initialize_population(num_nodes, k, population_size)

    best_solution = None
    best_score = float('inf')

    for generation in range(max_generations):

        scores = []
        for chromosome in population:
            score = calculate_conflicts(chromosome, edges)
            scores.append(score)

            if score < best_score:
                best_score = score
                best_solution = chromosome[:]


        if best_score == 0:
            break

        population = next_generation(population,scores,best_solution,k,population_size,mutation_rate,crossover_rate,tournament_selection)
    return best_solution

def find_min_colors(num_nodes, edges):
    start_time = time.time()
    for k in range(1, num_nodes + 1):
        for attempt in range(RETRIES):
            solution = run_genetic_algorithm(num_nodes,edges,k,POPULATION_SIZE,MAX_GENERATIONS,MUTATION_RATE,CROSSOVER_RATE)

            if calculate_conflicts(solution, edges) == 0:
                total_time = time.time() - start_time
                return solution, k, total_time

    total_time = time.time() - start_time
    return None, None, total_time

# Test Graph
num_nodes = 5

edges = [
    (0, 1),
    (0, 2),
    (1, 2),
    (1, 3),
    (2, 4),
    (3, 4)
]

# Run Genetic Algorithm
solution, min_k, total_time = find_min_colors(num_nodes, edges)

# Display Results
if solution is None:
    print("No solution found")
else:
    print("Best Coloring:", solution)
    print("Number of Colors:", min_k)
    print("Number of Conflicts:", calculate_conflicts(solution, edges))

print("Time:", round(total_time, 4), "seconds")