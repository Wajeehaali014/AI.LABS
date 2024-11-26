import random

# Define problem parameters
TABLES = [
    {"id": 1, "capacity": 4, "type": "window"},
    {"id": 2, "capacity": 2, "type": "standard"},
    {"id": 3, "capacity": 6, "type": "window"},
    {"id": 4, "capacity": 4, "type": "near_exit"},
    {"id": 5, "capacity": 2, "type": "standard"},
]

CUSTOMERS = [
    {"id": 1, "group_size": 4, "preference": "window"},
    {"id": 2, "group_size": 2, "preference": "standard"},
    {"id": 3, "group_size": 6, "preference": "window"},
    {"id": 4, "group_size": 2, "preference": "near_exit"},
    {"id": 5, "group_size": 2, "preference": "standard"},
]

# Genetic Algorithm parameters
POPULATION_SIZE = 20
GENERATIONS = 50
MUTATION_RATE = 0.2

class Individual:
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = self.calculate_fitness()

    @classmethod
    def create_random(cls):
        # Randomly assign customers to tables
        chromosome = [random.choice(TABLES)["id"] for _ in CUSTOMERS]
        return cls(chromosome)

    def calculate_fitness(self):
        # Fitness: Customer satisfaction score
        satisfaction = 0
        table_occupancy = {table["id"]: 0 for table in TABLES}

        for customer, table_id in zip(CUSTOMERS, self.chromosome):
            # Check if table can accommodate the group
            table = next(t for t in TABLES if t["id"] == table_id)
            if table_occupancy[table_id] + customer["group_size"] <= table["capacity"]:
                table_occupancy[table_id] += customer["group_size"]

                # Add satisfaction based on preference match
                if customer["preference"] == table["type"]:
                    satisfaction += 10
                else:
                    satisfaction += 5
            else:
                satisfaction -= 10  # Penalty for overcrowding

        return satisfaction

    def mate(self, other):
        # Crossover: Swap half of the chromosome
        point = random.randint(1, len(self.chromosome) - 1)
        child1 = self.chromosome[:point] + other.chromosome[point:]
        child2 = other.chromosome[:point] + self.chromosome[point:]
        return Individual(child1), Individual(child2)

    def mutate(self):
        # Randomly reassign one customer to a different table
        index = random.randint(0, len(self.chromosome) - 1)
        self.chromosome[index] = random.choice(TABLES)["id"]
        self.fitness = self.calculate_fitness()


def genetic_algorithm():
    # Initial population
    population = [Individual.create_random() for _ in range(POPULATION_SIZE)]
    best_individual = max(population, key=lambda x: x.fitness)

    for generation in range(GENERATIONS):
        # Sort population by fitness
        population.sort(key=lambda x: x.fitness, reverse=True)
        best_individual = max(population, key=lambda x: x.fitness)

        print(f"Generation {generation + 1}: Best Fitness = {best_individual.fitness}")

        # Create next generation
        new_generation = []

        # Elitism: Carry forward the top 2
        new_generation.extend(population[:2])

        # Generate new individuals through crossover and mutation
        while len(new_generation) < POPULATION_SIZE:
            parent1 = random.choice(population[:10])  # Favor top 10 individuals
            parent2 = random.choice(population[:10])
            child1, child2 = parent1.mate(parent2)

            if random.random() < MUTATION_RATE:
                child1.mutate()
            if random.random() < MUTATION_RATE:
                child2.mutate()

            new_generation.extend([child1, child2])

        population = new_generation[:POPULATION_SIZE]

    return best_individual


# Run the Genetic Algorithm
if __name__ == "__main__":
    best_solution = genetic_algorithm()
    print("\nBest Solution:")
    print(f"Chromosome: {best_solution.chromosome}")
    print(f"Fitness: {best_solution.fitness}")
