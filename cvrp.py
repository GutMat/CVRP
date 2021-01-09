# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 14:44:55 2021

@author: GutMa
"""

import random
from random import randrange
from time import time 

#=========================================================================== GENETIC ALGORITHM =======================================
# Class to represent problems to be solved by means of a general
# genetic algorithm. It includes the following attributes:
# - genes: list of possible genes in a chromosome
# - individuals_length: length of each chromosome
# - decode: method that receives the genotype (chromosome) as input and returns
#    the phenotype (solution to the original problem represented by the chromosome) 
# - fitness: method that returns the evaluation of a chromosome (acts over the
#    genotype)
# - mutation: function that implements a mutation over a chromosome
# - crossover: function that implements the crossover operator over two chromosomes
#=====================================================================================================================================

class Problem_Genetic(object):
    
    def __init__(self,genes,individuals_length,decode,fitness):
        self.genes= genes
        self.individuals_length= individuals_length
        self.decode= decode
        self.fitness= fitness

    def mutation(self, chromosome, prob):
            
            def inversion_mutation(chromosome_aux):
                chromosome = chromosome_aux
                
                index1 = randrange(0,len(chromosome))
                index2 = randrange(index1,len(chromosome))
                
                chromosome_mid = chromosome[index1:index2]
                chromosome_mid.reverse()
                
                chromosome_result = chromosome[0:index1] + chromosome_mid + chromosome[index2:]
                
                return chromosome_result
        
            aux = []
            for _ in range(len(chromosome)):
                if random.random() < prob :
                    aux = inversion_mutation(chromosome)
            return aux

    def crossover(self,parent1, parent2):

        def process_gen_repeated(copy_child1,copy_child2):
            count1=0
            for gen1 in copy_child1[:pos]:
                repeat = 0
                repeat = copy_child1.count(gen1)
                if repeat > 1:#If need to fix repeated gen
                    count2=0
                    for gen2 in parent1[pos:]:#Choose next available gen
                        if gen2 not in copy_child1:
                            child1[count1] = parent1[pos:][count2]
                        count2+=1
                count1+=1

            count1=0
            for gen1 in copy_child2[:pos]:
                repeat = 0
                repeat = copy_child2.count(gen1)
                if repeat > 1:#If need to fix repeated gen
                    count2=0
                    for gen2 in parent2[pos:]:#Choose next available gen
                        if gen2 not in copy_child2:
                            child2[count1] = parent2[pos:][count2]
                        count2+=1
                count1+=1

            return [child1,child2]

        pos=random.randrange(1,self.individuals_length-1)
        child1 = parent1[:pos] + parent2[pos:] 
        child2 = parent2[:pos] + parent1[pos:] 
        
        return  process_gen_repeated(child1, child2)
    
   
def decodeVRP(chromosome):    
    list=[]
    for (k,v) in chromosome:
        if k in trucks:
            list.append(frontier)
            continue
        list.append(cities.get(k))
    return list


def penalty_capacity(chromosome):
        actual = chromosome
        value_penalty = 0
        capacity_list = []
        index_cap = 0
        overloads = 0
        
        for i in range(0,len(trucks)+1):
            init = 0
            capacity_list.append(init)

            
        for (k,v) in actual:
            if k not in trucks:
                capacity_list[int(index_cap)]+=v
            else:
                index_cap+= 1
                
            if  capacity_list[index_cap] > capacity_trucks:
                overloads+=1
                value_penalty+= 100 * overloads
        return value_penalty

def fitnessVRP(chromosome):
    
    def distanceTrip(index,city):
        w = distances.get(index)
        return  w[city]
        
    actualChromosome = chromosome
    fitness_value = 0
   
    penalty_cap = penalty_capacity(actualChromosome)
    for (key,value) in actualChromosome:
        if key not in trucks:
            nextCity_tuple = actualChromosome[key]
            if list(nextCity_tuple)[0] not in trucks:
                nextCity= list(nextCity_tuple)[0]
                fitness_value+= distanceTrip(key,nextCity) + (50 * penalty_cap)
    return fitness_value


#========================================================== FIRST PART: GENETIC OPERATORS============================================
# Here We defined the requierements functions that the GA needs to work 
# The function receives as input:
# * problem_genetic: an instance of the class Problem_Genetic, with
#     the optimization problem that we want to solve.
# * k: number of participants on the selection tournaments.
# * opt: max or min, indicating if it is a maximization or a
#     minimization problem.
# * ngen: number of generations (halting condition)
# * size: number of individuals for each generation
# * ratio_cross: portion of the population which will be obtained by
#     means of crossovers. 
# * prob_mutate: probability that a gene mutation will take place.
#=====================================================================================================================================


def genetic_algorithm_t(Problem_Genetic,k,opt,ngen,size,ratio_cross,prob_mutate):
    
    def initial_population(Problem_Genetic,size):   
        def generate_chromosome():
            chromosome=[]
            for i in Problem_Genetic.genes:
                chromosome.append(i)
            random.shuffle(chromosome)
            return chromosome
        return [generate_chromosome() for _ in range(size)]
            
    def new_generation_t(Problem_Genetic,k,opt,population,n_parents,n_directs,prob_mutate):
        
        def tournament_selection(Problem_Genetic,population,n,k,opt):
            winners=[]
            for _ in range(n):
                elements = random.sample(population,k)
                winners.append(opt(elements,key=Problem_Genetic.fitness))
            return winners
        
        def cross_parents(Problem_Genetic,parents):
            childs=[]
            for i in range(0,len(parents),2):
                childs.extend(Problem_Genetic.crossover(parents[i],parents[i+1]))
            return childs
    
        def mutate(Problem_Genetic,population,prob):
            for i in population:
                Problem_Genetic.mutation(i,prob)
            return population
                        
        directs = tournament_selection(Problem_Genetic, population, n_directs, k, opt)
        crosses = cross_parents(Problem_Genetic,
                                tournament_selection(Problem_Genetic, population, n_parents, k, opt))
        mutations = mutate(Problem_Genetic, crosses, prob_mutate)
        new_generation = directs + mutations
        
        return new_generation
    
    population = initial_population(Problem_Genetic, size)
    n_parents = round(size*ratio_cross)
    n_parents = (n_parents if n_parents%2==0 else n_parents-1)
    n_directs = size - n_parents
    
    for _ in range(ngen):
        population = new_generation_t(Problem_Genetic, k, opt, population, n_parents, n_directs, prob_mutate)
    
    bestChromosome = opt(population, key = Problem_Genetic.fitness)
    print("Chromosome: ", bestChromosome)
    genotype = Problem_Genetic.decode(bestChromosome)
    print ("Solution: " , (genotype,Problem_Genetic.fitness(bestChromosome)))
    return (genotype,Problem_Genetic.fitness(bestChromosome))

 
#================================================THIRD PART: EXPERIMENTATION=========================================================
# Run over the same instances both the standard GA (from first part) as well as the modified version (from second part).
# Compare the quality of their results and their performance. Due to the inherent randomness of GA, the experiments performed over each instance should be run several times.
#====================================================================================================================================

#----------------------------------------MAIN PROGRAMA PRINCIPAL--------------------------------

def VRP(k):
    VRP_PROBLEM = Problem_Genetic([(0,500),(1,50),(2,400),(3,200),(4,100),(5,40),(6,200),(7,300),
                                   (8,30),(9,60),(10,50),(11,60),(12,160),(13,100),(14,120),
                                   (15,300),(16, 300),(17,100),
                                   (trucks[0],capacity_trucks), (trucks[1],capacity_trucks), (trucks[2],capacity_trucks), (trucks[3],capacity_trucks),(trucks[4],capacity_trucks)],
                                  len(cities), lambda x : decodeVRP(x), lambda y: fitnessVRP(y))
    
    def first_part_GA(k):
        best_solution = 999999999999
        tmp_genotype = None
        cont  = 0
        print ("---------------------------------------------------------Executing FIRST PART: VRP --------------------------------------------------------- \n")
        print("Capacity of trucks = ",capacity_trucks)
        print("Frontier = ",frontier)
        print("")
        tiempo_inicial_t2 = time()
        while cont <= k: 
            # genetic_algorithm_t(VRP_PROBLEM, 2, min, 200, 100, 0.8, 0.05)

            genotype, fitness = genetic_algorithm_t(VRP_PROBLEM, 2, min, 200, 100, 0.8, 0.05)
            if fitness < best_solution:
                best_solution = fitness
                tmp_genotype = genotype
            cont+=1
        
        print('Best:', best_solution)
        print('Genotype:', tmp_genotype)
        
        tiempo_final_t2 = time()
        print("\n") 
        print("Total time: ",(tiempo_final_t2 - tiempo_inicial_t2)," secs.\n")
        
    first_part_GA(k)

#---------------------------------------- AUXILIARY DATA FOR TESTING --------------------------------

#CONSTANTS

cities = {0:'Bialystok',1:'Bielsko_Biala',2:'Chrzanow',3:'Gdansk',4:'Gdynia',5:'Gliwice',6:'Gromnik',7:'Katowice',
          8:'Kielce',9:'Krosno',10:'Krynica',11:'Lublin',12:'Lodz',13:'Malbork',14:'Nowy_Targ',15:'Olsztyn',16:'Poznan',
          17:'Pulawy'}

#Distance between each pair of cities

dist_bialystok = [9999, 525, 477, 367, 389, 487, 455, 481, 347, 488, 510, 237, 320, 330, 531, 216, 498,290]
dist_bielsko_biala = [526, 9999, 49, 561, 583, 66, 153, 56, 182, 384, 174, 334, 246, 526, 103, 505, 435,346]
dist_chrzanow = [519, 50, 9999, 552, 576, 64, 143,36, 141, 393, 190, 332, 235, 537, 126, 504, 412,281]
dist_gdansk = [420, 586, 551, 9999,36,536, 690, 519, 468, 324, 737, 511, 340, 62, 674, 166, 310,472,472]
dist_gdynia = [453, 609, 574, 22,9999, 558, 713,542, 491,347, 760, 612, 363, 89, 697, 199, 362,578]
dist_gliwice = [501, 85, 62, 535, 559, 9999, 201, 28, 187, 329, 248, 377, 217, 519, 184,486, 348, 323]
dist_gromnik = [522,168,154,691,642,202,9999,174,141,531,59,290,296,602,121,541, 551, 230]
dist_katowice = [487,59,36,520,544,28,175,9999,159,361,222, 350, 203, 505, 159, 471, 376, 295]
dist_kielce = [369,212,141, 469,493, 184, 141, 159,9999, 375, 203, 193,147,453,210,388,362,140]
dist_krosno= [509, 414, 391,323, 375, 328, 530,355, 375, 9999,577, 497, 218, 336, 514, 355, 24, 460]
dist_krynica = [593,191,179, 742, 766, 250, 62, 222, 202, 582, 9999, 339, 422, 726, 104, 609,598, 289]
dist_lublin = [323, 404, 333, 507, 613, 376, 295,351, 193, 495, 352,9999, 305, 478, 410, 382, 483, 55]
dist_lodz = [316, 270, 235, 337, 361, 220,374, 203, 152, 231, 422, 303, 9999, 321, 358, 282, 205, 270]
dist_malbork = [391, 570, 536, 62, 91, 520, 675, 504, 452, 308, 722, 482, 317, 9999, 658, 137, 322, 443]
dist_nowy_targ = [579, 111, 126,676, 700, 187, 122, 159, 211, 516, 99, 420, 358, 660, 9999, 598, 534, 349]
dist_olsztyn = [223, 544, 510, 167, 202, 494, 556, 478, 388, 375, 605, 384, 291, 138, 597, 9999, 341, 346]
dist_poznan = [498,435,412,310,362,348,551,376,362,24,598,483,205,322,534,341,9999,447]
dist_pulawy = [290,346,281,472,578,323,230,295,140,460,289,55,270,443,349,346,447,9999]
distances = {0:dist_bialystok,1:dist_bielsko_biala,2:dist_chrzanow,3:dist_gdansk,4:dist_gdynia,5:dist_gliwice,
             6:dist_gromnik,7:dist_katowice,8:dist_kielce,9:dist_krosno,10:dist_krynica,11:dist_lublin,
             12:dist_lodz,13:dist_malbork,14:dist_nowy_targ,15:dist_olsztyn,16:dist_poznan,17:dist_pulawy}


capacity_trucks = 1000
trucks = ['truck_1','truck_2', 'truck_3','truck_4','truck_5']
num_trucks = len(trucks)
frontier = "---------"

if __name__ == "__main__":

    # Constant that is an instance object 
    genetic_problem_instances = 10
    print("EXECUTING ", genetic_problem_instances, " INSTANCES ")
    VRP(genetic_problem_instances)