import random
import math
from pyeasyga import pyeasyga

def read(file, lst):
    f=open(file)    
    for row in f:
        lst.append(row.replace('\n','').split(' '))
    f.close()
dataList=[]
read('./27data.txt',dataList)

massGlob=float(dataList[0][0])
vGlob=float(dataList[0][1])
dataSet=dataList[1:]
print('Mass: '+str(massGlob))
print('V: '+str(vGlob))

#my_list = [[1,'a'], [2,'b'], [0,'c']]
#my_list.sort(key=lambda val: int(val[0]))
#print(my_list)
print('DATA:')
for i in range(0,len(dataSet)):
    print(str(i)+': '+'; '.join(map(str, dataSet[i])))

#функция перевода v+mass+cost = приспособленность
def AVGfitness(item):
    mn=2/5;
    return mn*float(item[0])+mn*float(item[1])-(1-2*mn)*float(item[2])

dataVals=[] #list значений для расчета расстояния в OK
lenOK=[] #матрица расстояний между вещами рюкзака

for item in dataSet:
    dataVals.append(AVGfitness(item))
minVal=abs(min(dataVals))+1
for i in range(0,len(dataVals)):
    dataVals[i]+=minVal
for i in range(0,len(dataVals)):
    row = []
    for j in range(0,len(dataVals)):
        if i==j:
            row.append(100000000) # if index1==index2 val = inf
        else:
            row.append(abs(dataVals[i]-dataVals[j]))
    lenOK.append(row)

ga = pyeasyga.GeneticAlgorithm(dataSet,
                               population_size=100,
                               generations=60,
                               crossover_probability=0.99,
                               mutation_probability=0.10,
                               elitism=True,
                               maximise_fitness=True)

#Создание родителя
def create_individual(data):
    IndexHromosome = [random.randint(0, len(data)-1)]    
    global lenOK
    global massGlob
    global vGlob
    lenOKCopy=lenOK[:][:]
    for item in lenOKCopy:
        item[IndexHromosome[0]]=100000000
    boolHromosomeFind=0 
    while(not boolHromosomeFind):
        lastIndex=IndexHromosome[len(IndexHromosome)-1]
        currentOKrow = lenOKCopy[lastIndex]
        find=0        
        while(not find):            
            currentMinIndex = currentOKrow.index(min(currentOKrow))
            for item in lenOKCopy:
                item[currentMinIndex]=100000000
            theMass = float(data[currentMinIndex][0])
            theV = float(data[currentMinIndex][1])
            for i in IndexHromosome:
                theMass += float(data[i][0])
                theV += float(data[i][1])
            if(theMass>massGlob or theV>vGlob):
                boolHromosomeFind=1
            else:
                IndexHromosome.append(currentMinIndex)
            find=1
    Hromosome=[0]*len(data)
    for i in IndexHromosome:
        Hromosome[i]=1
    return Hromosome

def fitness (individual, data):
    global massGlob
    global vGlob
    fitnessMass = 0
    fitnessV = 0
    fitnessCost = 0
    fitnessMassAll = 0
    fitnessVAll = 0
    for (selected, (profit)) in zip(individual, data):
        if selected:
            fitnessMassAll +=float(profit[0])
            fitnessVAll +=float(profit[1])
            fitnessMass += 1/(float(profit[0])/10000)
            fitnessV += 1/(float(profit[1])*10)*100
            fitnessCost += float(profit[2])/10
            #print(profit[2]+' -> '+str(fitnessCost))
    avgfitness=fitnessMass+fitnessV+fitnessCost
    if fitnessMassAll>massGlob or fitnessVAll>vGlob:
        fitness=math.log(avgfitness,2)#AVGfitness([fitnessMass,fitnessV,fitnessCost]),2);
    else:
        fitness = avgfitness#AVGfitness([fitnessMass,fitnessV,fitnessCost])
    return fitness

def EquelMembers(member1,member2):
    pairs=zip(member1,member2)
    for pair in pairs:
        if pair[0]!=pair[1]:
            return 0
    return 1
def uniquePopulation(population):
    new_population=[population[0]]
    for member in population:
        i=0
        for member_new in new_population:
            if not EquelMembers(member,member_new):
                i+=1   
        if i==len(new_population):
           new_population.append(member) 
    return new_population

class MyChromosome:
    def __init__(self, genes):
        """Initialise the Chromosome."""
        self.genes = genes
        self.fitness = 0
    def __repr__(self):
        """Return initialised Chromosome representation in human readable form."""
        return repr((self.fitness, self.genes))
    
# define and set the GA's selection operation
# For the selection function, supply a ``population`` parameter
def selection(population):
    global dataSet
    this_population = []
    for member in population:
        this_population.append(member.genes)
    unique_population = uniquePopulation(this_population)
    #высчитываем приспособленность для уникальных особей
    fitnessPopulation = []
    sum_fitnessPopulation = 0
    for member in unique_population:
        member_fitness = fitness(member,dataSet)
        fitnessPopulation.append([member_fitness,member])
        sum_fitnessPopulation += member_fitness
    #высчитываем P для особей
    N = len(unique_population)
    population_P=[]
    for i in range(0,N):
        population_P.append(fitnessPopulation[i][0]/sum_fitnessPopulation)
    #Бросаем рулетку
    roulette = random.random();
    #Находим i диапазон
    i = 0
    minVal=0
    maxVal=population_P[i]
    while not (minVal <= roulette < maxVal):
        minVal = minVal+population_P[i]
        i+=1
        maxVal= minVal+population_P[i]
        #print(str(minVal)+' -> '+str(maxVal)+' :'+str(i))
    return MyChromosome(unique_population[i])

# For the crossover function, supply two individuals (i.e. candidate
# solution representations) as parameters,
def crossover(parent_1, parent_2):
    child_1 = []
    child_2 = []
    parents=[parent_1,parent_2]
    for i in range(0,len(parent_1)):
        crossover_parent = random.randint(0, 1)
        child_1.append(parents[crossover_parent][i])
        crossover_parent = random.randint(0, 1)
        child_2.append(parents[crossover_parent][i])
    return child_1, child_2

# For the mutate function, supply one individual (i.e. a candidate
# solution representation) as a parameter,
def mutate(individual):
    mutate_index = random.randrange(len(individual))
    while individual[mutate_index] == 1:
        mutate_index = random.randrange(len(individual))
    individual[mutate_index] == 1

# and set the Genetic Algorithm's ``mutate_function`` attribute to
# your defined function
ga.mutate_function = mutate

# and set the Genetic Algorithm's ``crossover_function`` attribute to
# your defined function
ga.crossover_function = crossover

# and set the Genetic Algorithm's ``create_individual`` attribute to
# your defined function
ga.create_individual = create_individual

# and set the Genetic Algorithm's ``selection_function`` attribute to
# your defined function
ga.selection_function = selection

# and set the Genetic Algorithm's ``fitness_function`` attribute to
# your defined function
ga.fitness_function = fitness

ga.run()
print (ga.best_individual())
#print(1+(math.log((1/(1-math.pow(0.99999999999999,1/30))),2)))

mass=0
V=0
cost=0
ans = ga.best_individual()

for (select, (profit)) in zip(ans[1], dataSet):
        if select:
            mass += float(profit[0])
            V += float(profit[1])
            cost += float(profit[2])
            
print('Mass: '+str(massGlob))
print('V: '+str(vGlob))
print('Mass_ans: '+str(mass))
print('V_ans: '+str(V))
print('Cost_ans: '+str(cost))

        
