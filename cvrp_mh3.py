import random
from random import randrange
from time import time

# Klasa odpowiadajaca za procesy mutowania, krzyzowania
# oraz dekodowania chromosomow. Zawarte sa rowniez funkcje
# odpowiedzialne za obliczanie wartosci kary wykorzystywanej
# w funkcji dopasowania


class GeneticAlgorithm(object):

    # Inicjalizacja obiektu
    def __init__(self, genes, cities, decode, fitness):
        self.genes = genes
        self.cities_len = len(cities)
        self.decode = decode
        self.fitness = fitness

    # Funkcja mutujaca chromosome
    def mutation(self, chromosome, probability):

        # Funkcja wykorzystujaca inwersje w chromosomie
        # poprzez wylosowanie obszaru do odwrocenia
        def inversion_mutation(chromosome):

            index_1 = randrange(0, len(chromosome))
            index_2 = randrange(index_1, len(chromosome))

            chromosome_segment = chromosome[index_1:index_1]
            chromosome_segment.reverse()

            inversed_chromosome = chromosome[0:index_1] + \
                chromosome_segment + chromosome[index_2:]

            return inversed_chromosome

        # Petla, odpowiadajaca za mozliwosc
        # zmutowania chromosomu w oparciu o
        # ustalone prawdopodobienstwo
        mutated_chromosome = []
        for _ in range(len(chromosome)):
            if random.random() < probability:
                mutated_chromosome = inversion_mutation(chromosome)
        return mutated_chromosome

    # Funkcja odpowiadajaca za procesy krzyzowania
    # chromosomow. Zawiera funkcje walidacyjna, pozwalajaca
    # na sprawdzenie poprawnosci chromosomu
    def crossover(self, parent1, parent2):

        def gene_validation(offspring_1, offspring_2):

            index_1 = 0
            # Petla sprawdzajaca powtorzenia chromosomow
            # dla pierwszego potomka
            for gene_1 in offspring_1[:position]:
                repeat = 0
                repeat = offspring_1.count(gene_1)
                # Jesli sie powtarza
                if repeat > 1:
                    index_2 = 0
                    # Znajdz nastepny dostepny
                    for gene_2 in parent1[position:]:
                        if gene_2 not in offspring_1:
                            child1[index_1] = parent1[position:][index_2]
                        index_2 += 1
                index_1 += 1

            index_1 = 0
            # Petla sprawdzajaca powtorzenia chromosomow
            # dla drugiego potomka
            for gene_1 in offspring_2[:position]:
                repeat = 0
                repeat = offspring_2.count(gene_1)
                if repeat > 1:
                    index_2 = 0
                    for gene_2 in parent2[position:]:
                        if gene_2 not in offspring_2:
                            child2[index_1] = parent2[position:][index_2]
                        index_2 += 1
                index_1 += 1

            return [child1, child2]

        # Pozycja krzyzowania chromosomow
        position = random.randrange(1, self.cities_len-1)
        child1 = parent1[:position] + parent2[position:]
        child2 = parent2[:position] + parent1[position:]

        return gene_validation(child1, child2)

# Funkcja do dekodowania chromosomow
# do czytelnego formatu


def chromosome_decoder(chromosome):
    list = []
    for (key, value) in chromosome:
        if key in trucks:
            list.append(frontier)
            continue
        list.append(cities.get(key))
    return list

# Funkcja obliczajaca kare jesli przekroczona
# jest maksymalna ladownosc auta


def count_capacity_penalty(chromosome):
    penalty_value = 0
    capacity_list = [0] * len(trucks)
    capacity_index = 0
    overflow = 0

    for (key, value) in chromosome:
        if key not in trucks:
            capacity_list[int(capacity_index)] += value
        else:
            capacity_index += 1

        if capacity_list[capacity_index] > trucks_capacity:
            overflow += 1
            penalty_value += 100 * overflow
    return penalty_value

# Funkcja obliczajaca wartosc funkcji dopasowania


def count_fitness_value(chromosome):

    def get_city_distance(key, city_index):
        city_vector = distances.get(key)
        return city_vector[city_index]

    fitness_value = 0

    penalty_value = count_capacity_penalty(chromosome)
    for (key, value) in chromosome:
        if key not in trucks:
            city_gene = chromosome[key]
            if city_gene[0] not in trucks:
                city_index = city_gene[0]
                fitness_value += get_city_distance(key,
                                                   city_index) + (50 * penalty_value)
    return fitness_value


def genetic_algorithm_process(GeneticAlgorithm, selection_tournament_number, generation_number, population_size, cross_ratio, mutation_probability):

    def initial_population(GeneticAlgorithm, population_size):
        def generate_chromosome():
            chromosome = []
            for gene in GeneticAlgorithm.genes:
                chromosome.append(gene)
            random.shuffle(chromosome)
            return chromosome
        return [generate_chromosome() for _ in range(population_size)]

    def get_new_generation(GeneticAlgorithm, selection_tournament_number, population, n_parents, n_directs, mutation_probability):

        def tournament_selection(GeneticAlgorithm, population, n_directs, selection_tournament_number):
            winners = []
            for _ in range(n_directs):
                elements = random.sample(
                    population, selection_tournament_number)
                winners.append(min(elements, key=GeneticAlgorithm.fitness))
            return winners

        def cross_parents(GeneticAlgorithm, parents):
            childs = []
            for index in range(0, len(parents), 2):
                childs.extend(GeneticAlgorithm.crossover(
                    parents[index], parents[index+1]))
            return childs

        def mutate(GeneticAlgorithm, population, probability):
            for index in population:
                GeneticAlgorithm.mutation(index, probability)
            return population

        directs = tournament_selection(
            GeneticAlgorithm, population, n_directs, selection_tournament_number)
        crosses = cross_parents(GeneticAlgorithm,
                                tournament_selection(GeneticAlgorithm, population, n_parents, selection_tournament_number))
        mutations = mutate(GeneticAlgorithm, crosses, mutation_probability)
        new_generation = directs + mutations

        return new_generation

    population = initial_population(GeneticAlgorithm, population_size)
    n_parents = round(population_size*cross_ratio)
    n_parents = (n_parents if n_parents % 2 == 0 else n_parents-1)
    n_directs = population_size - n_parents

    for _ in range(generation_number):
        population = get_new_generation(
            GeneticAlgorithm, selection_tournament_number, population, n_parents, n_directs, mutation_probability)

    best_chromosome = min(population, key=GeneticAlgorithm.fitness)
    print("Chromosome: ", best_chromosome)
    genotype = GeneticAlgorithm.decode(best_chromosome)
    print("Solution: ", (genotype, GeneticAlgorithm.fitness(best_chromosome)))
    return (genotype, GeneticAlgorithm.fitness(best_chromosome))


def VRP(k):
    VRP_PROBLEM = GeneticAlgorithm([(0, 500), (1, 50), (2, 400), (3, 200), (4, 100), (5, 40), (6, 200), (7, 300),
                                    (8, 30), (9, 60), (10, 50), (11,
                                                                 60), (12, 160), (13, 100), (14, 120),
                                    (15, 300), (16, 300), (17, 100),
                                    (trucks[0], trucks_capacity), (trucks[1], trucks_capacity), (trucks[2], trucks_capacity), (trucks[3], trucks_capacity)],
                                   cities, lambda x: chromosome_decoder(x), lambda y: count_fitness_value(y))

    def first_part_GA(k):
        best_solution = 999999999999
        best_tour = None
        cont = 0
        print("---------------------------------------------------------Executing FIRST PART: VRP --------------------------------------------------------- \n")
        print("Capacity of trucks = ", trucks_capacity)
        print("Frontier = ", frontier)
        print("")
        tiempo_inicial_t2 = time()
        while cont <= k:
            # genetic_algorithm_t(VRP_PROBLEM, 2, min, 200, 100, 0.8, 0.05)

            genotype, fitness = genetic_algorithm_process(
                VRP_PROBLEM, 2, 200, 100, 0.8, 0.05)
            if fitness < best_solution:
                best_solution = fitness
                best_tour = genotype
            cont += 1

        print('Best:', best_solution)
        print('Genotype:', best_tour)

        tiempo_final_t2 = time()
        print("\n")
        print("Total time: ", (tiempo_final_t2 - tiempo_inicial_t2), " secs.\n")

    first_part_GA(k)

# ---------------------------------------- AUXILIARY DATA FOR TESTING --------------------------------

# CONSTANTS


cities = {0: 'Bialystok', 1: 'Bielsko_Biala', 2: 'Chrzanow', 3: 'Gdansk', 4: 'Gdynia', 5: 'Gliwice', 6: 'Gromnik', 7: 'Katowice',
          8: 'Kielce', 9: 'Krosno', 10: 'Krynica', 11: 'Lublin', 12: 'Lodz', 13: 'Malbork', 14: 'Nowy_Targ', 15: 'Olsztyn', 16: 'Poznan',
          17: 'Pulawy'}

# Distance between each pair of cities

dist_bialystok = [9999, 525, 477, 367, 389, 487, 455,
                  481, 347, 488, 510, 237, 320, 330, 531, 216, 498, 290]
dist_bielsko_biala = [526, 9999, 49, 561, 583, 66, 153,
                      56, 182, 384, 174, 334, 246, 526, 103, 505, 435, 346]
dist_chrzanow = [519, 50, 9999, 552, 576, 64, 143, 36,
                 141, 393, 190, 332, 235, 537, 126, 504, 412, 281]
dist_gdansk = [420, 586, 551, 9999, 36, 536, 690, 519,
               468, 324, 737, 511, 340, 62, 674, 166, 310, 472, 472]
dist_gdynia = [453, 609, 574, 22, 9999, 558, 713, 542,
               491, 347, 760, 612, 363, 89, 697, 199, 362, 578]
dist_gliwice = [501, 85, 62, 535, 559, 9999, 201, 28,
                187, 329, 248, 377, 217, 519, 184, 486, 348, 323]
dist_gromnik = [522, 168, 154, 691, 642, 202, 9999, 174,
                141, 531, 59, 290, 296, 602, 121, 541, 551, 230]
dist_katowice = [487, 59, 36, 520, 544, 28, 175, 9999,
                 159, 361, 222, 350, 203, 505, 159, 471, 376, 295]
dist_kielce = [369, 212, 141, 469, 493, 184, 141, 159,
               9999, 375, 203, 193, 147, 453, 210, 388, 362, 140]
dist_krosno = [509, 414, 391, 323, 375, 328, 530, 355,
               375, 9999, 577, 497, 218, 336, 514, 355, 24, 460]
dist_krynica = [593, 191, 179, 742, 766, 250, 62, 222,
                202, 582, 9999, 339, 422, 726, 104, 609, 598, 289]
dist_lublin = [323, 404, 333, 507, 613, 376, 295, 351,
               193, 495, 352, 9999, 305, 478, 410, 382, 483, 55]
dist_lodz = [316, 270, 235, 337, 361, 220, 374, 203,
             152, 231, 422, 303, 9999, 321, 358, 282, 205, 270]
dist_malbork = [391, 570, 536, 62, 91, 520, 675, 504,
                452, 308, 722, 482, 317, 9999, 658, 137, 322, 443]
dist_nowy_targ = [579, 111, 126, 676, 700, 187, 122, 159,
                  211, 516, 99, 420, 358, 660, 9999, 598, 534, 349]
dist_olsztyn = [223, 544, 510, 167, 202, 494, 556, 478,
                388, 375, 605, 384, 291, 138, 597, 9999, 341, 346]
dist_poznan = [498, 435, 412, 310, 362, 348, 551, 376,
               362, 24, 598, 483, 205, 322, 534, 341, 9999, 447]
dist_pulawy = [290, 346, 281, 472, 578, 323, 230, 295,
               140, 460, 289, 55, 270, 443, 349, 346, 447, 9999]
distances = {0: dist_bialystok, 1: dist_bielsko_biala, 2: dist_chrzanow, 3: dist_gdansk, 4: dist_gdynia, 5: dist_gliwice,
             6: dist_gromnik, 7: dist_katowice, 8: dist_kielce, 9: dist_krosno, 10: dist_krynica, 11: dist_lublin,
             12: dist_lodz, 13: dist_malbork, 14: dist_nowy_targ, 15: dist_olsztyn, 16: dist_poznan, 17: dist_pulawy}


trucks_capacity = 1000
trucks = ['truck_1', 'truck_2', 'truck_3', 'truck_4', 'truck_5']
num_trucks = len(trucks)
frontier = "---------"

if __name__ == "__main__":

    # Constant that is an instance object
    genetic_problem_instances = 100
    print("EXECUTING ", genetic_problem_instances, " INSTANCES ")
    VRP(genetic_problem_instances)
