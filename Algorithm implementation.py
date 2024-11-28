import random

ingredients = [
    ('Chicken', 165, 31, 3.6),
    ('Salmon', 208, 22, 12),
    ('Broccoli', 55, 4, 0.6),
    ('Rice', 206, 4, 0.4),
    ('Avocado', 240, 3, 22),
    ('Egg', 68, 6, 4.8),
    ('Spinach', 23, 3, 0.4),
    ('Almonds', 579, 21, 49)
]

target_calories = 2000
target_protein = 100
target_fat = 70

def fitness(diet_plan):
    total_calories = sum([ingredients[i][1] for i in diet_plan])
    total_protein = sum([ingredients[i][2] for i in diet_plan])
    total_fat = sum([ingredients[i][3] for i in diet_plan])
    calorie_penalty = abs(total_calories - target_calories) / target_calories
    protein_penalty = abs(total_protein - target_protein) / target_protein
    fat_penalty = abs(total_fat - target_fat) / target_fat
    return calorie_penalty + protein_penalty + fat_penalty

def create_population(population_size, diet_length):
    population = []
    for _ in range(population_size):
        diet_plan = random.sample(range(len(ingredients)), diet_length)
        population.append(diet_plan)
    return population

def select_parents(population):
    fitness_scores = [fitness(diet) for diet in population]
    total_fitness = sum(fitness_scores)
    probabilities = [1 - (score / total_fitness) for score in fitness_scores]
    parent1 = random.choices(population, weights=probabilities, k=1)[0]
    parent2 = random.choices(population, weights=probabilities, k=1)[0]
    return parent1, parent2

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child

def mutate(diet_plan, mutation_rate):
    if random.random() < mutation_rate:
        if random.random() < 0.5:
            diet_plan.append(random.randint(0, len(ingredients) - 1))
        else:
            if len(diet_plan) > 1:
                diet_plan.pop(random.randint(0, len(diet_plan) - 1))
    return diet_plan

def genetic_algorithm(population_size, diet_length, generations, mutation_rate):
    population = create_population(population_size, diet_length)
    best_diet_plan = min(population, key=fitness)
    for generation in range(generations):
        new_population = []
        for _ in range(population_size):
            parent1, parent2 = select_parents(population)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            new_population.append(child)
        population = new_population
        current_best = min(population, key=fitness)
        if fitness(current_best) < fitness(best_diet_plan):
            best_diet_plan = current_best
        print(f"Generation {generation + 1}: Best Diet = {[ingredients[i][0] for i in current_best]}, Fitness = {fitness(current_best)}")
    return best_diet_plan

best_diet_plan = genetic_algorithm(population_size=10, diet_length=5, generations=10, mutation_rate=0.1)

print("\nFinal Best Diet Plan:")
for index in best_diet_plan:
    name, calories, protein, fat = ingredients[index]
    print(f"{name}: Calories={calories}, Protein={protein}, Fat={fat}")

print("\nFinal Fitness Score:", fitness(best_diet_plan))
