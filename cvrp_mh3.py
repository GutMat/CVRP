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
            list.append(separator)
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
            capacity_list[capacity_index] += value
        else:
            capacity_index += 1

        if capacity_list[capacity_index] > trucks_capacity:
            overflow += 1
            penalty_value += 100 * overflow
    return penalty_value

# Funkcja obliczajaca wartosc funkcji dopasowania


def count_fitness_value(chromosome):

    # Funkcja zwracajaca odleglosc pomiedzy wybranymi miastami
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


def genetic_algorithm_process(GeneticAlgorithm, selection_tournament_number, generation_number, population_size, cross_ratio, mutation_probability, counter):
    # Funkcja inicjujaca startowa populacje,
    # rozmiar populacji ustalany jest za posrednictwem
    # parametru population_size
    def initial_population(GeneticAlgorithm, population_size):
        # Funkcja generujaca pojedynczny chromosome
        def generate_chromosome():
            chromosome = []
            for gene in GeneticAlgorithm.genes:
                chromosome.append(gene)
            random.shuffle(chromosome)
            return chromosome
        return [generate_chromosome() for _ in range(population_size)]

    def get_new_generation(GeneticAlgorithm, selection_tournament_number, population, n_parents, number_rest, mutation_probability):

        # Funkcja odpowiadajaca za wybor najlepszych
        # za pomoca turniejowej selekcji, liczba wybranych
        # chromosomow ustalana jest za pomoca parametru
        # selection_tournament_number
        def tournament_selection(GeneticAlgorithm, population, number_rest, selection_tournament_number):
            winners = []
            for _ in range(number_rest):
                elements = random.sample(
                    population, selection_tournament_number)
                winners.append(min(elements, key=GeneticAlgorithm.fitness))
            return winners

        # Funkcja odpowiadajaca za krzyzowanie osobnikow
        def cross_parents(GeneticAlgorithm, parents):
            childs = []
            for index in range(0, len(parents), 2):
                childs.extend(GeneticAlgorithm.crossover(
                    parents[index], parents[index+1]))
            return childs

        # Funkcja odpowiadajaca za mutowanie, czestotliwosc
        # mutacji ustalana jest za pomoca parametru
        # probability
        def mutate(GeneticAlgorithm, population, probability):
            for index in population:
                GeneticAlgorithm.mutation(index, probability)
            return population

        directs = tournament_selection(
            GeneticAlgorithm, population, number_rest, selection_tournament_number)
        crosses = cross_parents(GeneticAlgorithm,
                                tournament_selection(GeneticAlgorithm, population, n_parents, selection_tournament_number))
        mutations = mutate(GeneticAlgorithm, crosses, mutation_probability)
        new_generation = directs + mutations

        return new_generation

    # Inicjalizacja populacji
    population = initial_population(GeneticAlgorithm, population_size)

    # Ustalenie liczby rodzicow, za pomoca parametru
    # cross_ratio, ktory wplywa na rozklad populacji
    # i ilosc krzyzowanych osobnikow
    number_parents = round(population_size*cross_ratio)
    number_parents = (number_parents if number_parents %
                      2 == 0 else number_parents-1)
    number_rest = population_size - number_parents

    # Generowanie generacji w zaleznosci od ustalonego
    # parametru generation_number
    for _ in range(generation_number):
        population = get_new_generation(
            GeneticAlgorithm, selection_tournament_number, population, number_parents, number_rest, mutation_probability)

    best_chromosome = min(population, key=GeneticAlgorithm.fitness)
    print("Epoka numer:", counter)
    print("Chromosom: ", best_chromosome)
    genotype = GeneticAlgorithm.decode(best_chromosome)
    print("Rozwiazanie: ", (genotype, GeneticAlgorithm.fitness(best_chromosome)))
    return (genotype, GeneticAlgorithm.fitness(best_chromosome))


def CVRP(number_epochs, selection_tournament_number, generation_number, population_size, cross_ratio, mutation_probability):
    # Inicjalizacja obiektu klasy GeneticAlgorithm
    # pozwalajacego wykonywac caly proces obliczania
    # najlepszego rozwiazania
    CVRP_GA = GeneticAlgorithm([(0, 500), (1, 50), (2, 400), (3, 200), (4, 100), (5, 40), (6, 200), (7, 300),
                                (8, 30), (9, 60), (10, 50), (11,
                                                             60), (12, 160), (13, 100), (14, 120),
                                (15, 300), (16, 100), (17, 200), (18,
                                                                  100), (19, 60), (20, 200), (21, 150),
                                (22, 60), (23, 50), (24, 70), (25,
                                                               200), (26, 90), (27, 40),
                                (28, 200), (29, 300),
                                (trucks[0], trucks_capacity),
                                (trucks[1], trucks_capacity),
                                (trucks[2], trucks_capacity),
                                (trucks[3], trucks_capacity)
                                ],
                               cities, lambda x: chromosome_decoder(x), lambda y: count_fitness_value(y))

    best_solution = 999999999999
    best_tour = None
    counter = 0
    print("Uruchomiono program CVRP")
    print("Liczba epok wynosi:", number_epochs)
    print("Liczba wybieranych zwyciezcow wynosi:", selection_tournament_number)
    print("Liczba generacji wynosi:", generation_number)
    print("Wielkosc populacji wynosi:", population_size)
    print("Stosunek krzyzowanych rodzicow wynosi:", cross_ratio)
    print("Prawdopodobienstwo mutacji wynosi:", mutation_probability)
    print("Pojemnosc ciezarowek wynosi: ", trucks_capacity)
    execution_time_start = time()
    while counter <= number_epochs:
        genotype, fitness = genetic_algorithm_process(
            CVRP_GA, selection_tournament_number, generation_number, population_size, cross_ratio, mutation_probability, counter)
        if fitness < best_solution:
            best_solution = fitness
            best_tour = genotype
        counter += 1

    print('Najlepsze wynik rozwiazania:', best_solution)
    print('Najlepsza trasa dla poszczegolnych ciezarowek:', best_tour)

    execution_time_end = time()
    print("\n")
    print("Calkowity czas wykonania: ",
          (execution_time_end - execution_time_start), " sekund.\n")


# Slownik zawierajacy nazwy miejscowosci
cities = {0: 'Bialystok', 1: 'Bielsko_Biala', 2: 'Chrzanow', 3: 'Gdansk', 4: 'Gdynia', 5: 'Gliwice', 6: 'Gromnik', 7: 'Katowice',
          8: 'Kielce', 9: 'Krosno', 10: 'Krynica', 11: 'Lublin', 12: 'Lodz', 13: 'Malbork', 14: 'Nowy_Targ', 15: 'Olsztyn', 16: 'Poznan',
          17: 'Pulawy', 18: 'Radom', 19: 'Rzeszow', 20: 'Sandomierz', 21: 'Szczecin', 22: 'Szczucin',
          23: 'Szklarska_Poreba', 24: 'Tarnow', 25: 'Warszawa', 26: 'Wieliczka', 27: 'Wroclaw',
          28: 'Zakopane', 29: 'Zamosc'}

# Wektory reprezentujace macierz odleglosci
# w oparciu o dane pozyskane z heuristic lab

dist_bialystok = [99999, 429, 417, 315, 341, 418, 335, 426, 250, 351, 409, 203, 261,
                  294, 442, 203, 390, 176, 222, 354, 243, 557, 336, 544, 374, 179, 361, 481, 455, 225]

dist_bielsko_biala = [429, 99999, 44, 470, 501, 14, 178, 9, 182, 228, 194, 295, 216,
                      411, 94, 453, 279, 287, 209, 257, 238, 470, 145, 253, 186, 261, 78, 170, 145, 319]
dist_chrzanow = [417, 44, 99999, 488, 520, 49, 139, 51, 167, 187, 151, 266, 228,
                 430, 56, 460, 311, 264, 196, 215, 209, 507, 109, 296, 143, 259, 57, 213, 105, 287]
dist_gdansk = [315, 470, 488, 99999, 34, 456, 497, 462, 374, 541, 571, 439, 263, 59,
               538, 117, 236, 400, 356, 559, 440, 288, 474, 417, 538, 278, 445, 403, 576, 476]
dist_gdynia = [341, 501, 520, 34, 99999, 488, 531, 493, 408, 575, 604, 471, 296, 91,
               570, 139, 260, 432, 389, 593, 473, 288, 508, 437, 571, 311, 477, 428, 609, 508]
dist_gliwice = [418, 14, 49, 456, 488, 99999, 177, 8, 172, 228, 198, 288, 203, 398,
                103, 439, 267, 279, 199, 257, 232, 460, 143, 248, 188, 249, 73, 164, 153, 313]
dist_gromnik = [335, 178, 139, 497, 531, 177, 99999, 182, 123, 57, 78, 148, 245,
                443, 130, 438, 379, 161, 145, 85, 95, 588, 37, 417, 43, 225, 110, 331, 124, 157]
dist_katowice = [426, 9, 51, 462, 493, 8, 182, 99999, 180, 233, 201, 295, 210, 403,
                 102, 446, 270, 287, 207, 262, 239, 461, 148, 246, 192, 257, 79, 162, 153, 320]
dist_kielce = [250, 182, 167, 374, 408, 172, 123, 180, 99999, 170, 198, 132, 128,
               321, 197, 319, 277, 113, 29, 191, 91, 486, 104, 360, 164, 105, 111, 279, 219, 168]
dist_krosno = [351, 228, 187, 541, 575, 228, 57, 233, 170, 99999, 69, 150, 295,
               489, 164, 474, 434, 175, 186, 29, 112, 643, 93, 472, 48, 265, 164, 386, 141, 144]
dist_krynica = [409, 194, 151, 571, 604, 198, 78, 201, 198, 69, 99999, 213, 314,
                516, 112, 515, 436, 233, 221, 87, 167, 642, 97, 446, 36, 302, 150, 362, 77, 212]
dist_lublin = [203, 295, 266, 439, 471, 288, 148, 295, 132, 150, 213, 99999, 239,
               395, 273, 353, 396, 40, 122, 151, 58, 601, 163, 491, 181, 171, 217, 411, 271, 41]
dist_lodz = [261, 216, 228, 263, 296, 203, 245, 210, 128, 295, 314, 239, 99999, 206,
             276, 237, 158, 206, 122, 318, 213, 363, 217, 285, 283, 87, 182, 222, 314, 279]
dist_malbork = [294, 411, 430, 59, 91, 398, 443, 403, 321, 489, 516, 395, 206, 99999,
                480, 117, 185, 356, 304, 508, 391, 275, 419, 368, 484, 228, 387, 348, 519, 434]
dist_nowy_targ = [442, 94, 56, 538, 570, 103, 130, 102, 197, 164, 112, 273, 276, 480,
                  99999, 504, 366, 278, 226, 190, 216, 562, 111, 344, 117, 296, 95, 262, 51, 286]
dist_olsztyn = [203, 453, 460, 117, 139, 439, 438, 446, 319, 474, 515, 353, 237, 117,
                504, 99999, 282, 315, 294, 488, 366, 390, 422, 464, 480, 214, 410, 429, 535, 387]
dist_poznan = [390, 279, 311, 236, 260, 267, 379, 270, 277, 434, 436, 396, 158, 185,
               366, 282, 99999, 364, 277, 460, 366, 210, 346, 185, 411, 238, 288, 170, 413, 436]
dist_pulawy = [176, 287, 264, 400, 432, 279, 161, 287, 113, 175, 233, 40, 206, 356,
               278, 315, 364, 99999, 95, 181, 67, 566, 168, 468, 199, 134, 211, 390, 284, 78]
dist_radom = [222, 209, 196, 356, 389, 199, 145, 207, 29, 186, 221, 122, 122, 304,
              226, 294, 277, 95, 99999, 205, 92, 484, 129, 374, 186, 81, 140, 296, 247, 160]
dist_rzeszow = [354, 257, 215, 559, 593, 257, 85, 262, 191, 29, 87, 151, 318, 508,
                190, 488, 460, 181, 205, 99999, 123, 669, 121, 500, 74, 282, 193, 415, 163, 138]
dist_sandomierz = [243, 238, 209, 440, 473, 232, 95, 239, 91, 112, 167, 58, 213,
                   391, 216, 366, 366, 67, 92, 123, 99999, 574, 106, 445, 132, 163, 161, 363, 218, 82]
dist_szczecin = [557, 470, 507, 288, 288, 460, 588, 461, 486, 643, 642, 601, 363, 275,
                 562, 390, 210, 566, 484, 669, 574, 99999, 554, 268, 619, 435, 492, 318, 611, 641]
dist_szczucin = [336, 145, 109, 474, 508, 143, 37, 148, 104, 93, 97, 163, 217, 419,
                 111, 422, 346, 168, 129, 121, 106, 554, 99999, 381, 67, 208, 74, 295, 120, 179]
dist_szklarska_poreba = [544, 253, 296, 417, 437, 248, 417, 246, 360, 472, 446, 491, 285,
                         368, 344, 464, 185, 468, 374, 500, 445, 268, 381, 99999, 434, 371, 308, 86, 394, 526]
dist_tarnow = [374, 186, 143, 538, 571, 188, 43, 192, 164, 48, 36, 181, 283, 484,
               117, 480, 411, 199, 186, 74, 132, 619, 67, 434, 99999, 267, 130, 349, 96, 183]
dist_warszawa = [179, 261, 259, 278, 311, 249, 225, 257, 105, 265, 302, 171, 87, 228,
                 296, 214, 238, 134, 81, 282, 163, 435, 208, 371, 267, 99999, 204, 304, 323, 211]
dist_wieliczka = [361, 78, 57, 445, 477, 73, 110, 79, 111, 164, 150, 217, 182, 387,
                  95, 410, 288, 211, 140, 193, 161, 492, 74, 308, 130, 204, 99999, 222, 133, 241]
dist_wroclaw = [481, 170, 213, 403, 428, 164, 331, 162, 279, 386, 362, 411, 222, 348,
                262, 429, 170, 390, 296, 415, 363, 318, 295, 86, 349, 304, 222, 99999, 313, 444]
dist_zakopane = [455, 145, 105, 576, 609, 153, 124, 153, 219, 141, 77, 271, 314, 519,
                 51, 535, 413, 284, 247, 163, 218, 611, 120, 394, 96, 323, 133, 313, 99999, 277]
dist_zamosc = [225, 319, 287, 476, 508, 313, 157, 320, 168, 144, 212, 41, 279, 434,
               286, 387, 436, 78, 160, 138, 82, 641, 179, 526, 183, 211, 241, 444, 277, 99999]
distances = {0: dist_bialystok, 1: dist_bielsko_biala, 2: dist_chrzanow, 3: dist_gdansk, 4: dist_gdynia, 5: dist_gliwice,
             6: dist_gromnik, 7: dist_katowice, 8: dist_kielce, 9: dist_krosno, 10: dist_krynica, 11: dist_lublin,
             12: dist_lodz, 13: dist_malbork, 14: dist_nowy_targ, 15: dist_olsztyn, 16: dist_poznan, 17: dist_pulawy,
             18: dist_radom, 19: dist_rzeszow, 20: dist_sandomierz, 21: dist_szczecin, 22: dist_szczucin,
             23: dist_szklarska_poreba, 24: dist_tarnow, 25: dist_warszawa, 26: dist_wieliczka, 27: dist_wroclaw,
             28: dist_zakopane, 29: dist_zamosc}


trucks_capacity = 1000
trucks = ['Ciezarowka_1', 'Ciezarowka_2',
          'Ciezarowka_3', 'Ciezarowka_4', 'Ciezarowka_5']
num_trucks = len(trucks)
separator = "#***#"

if __name__ == "__main__":

    number_epochs = 10
    selection_tournament_number = 2
    generation_number = 200
    population_size = 100
    cross_ratio = 0.8
    mutation_probability = 0.05
    CVRP(number_epochs, selection_tournament_number, generation_number,
         population_size, cross_ratio, mutation_probability)
