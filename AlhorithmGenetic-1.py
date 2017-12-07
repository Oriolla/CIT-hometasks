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
data=dataList[1:]
print('Mass: '+str(massGlob))
print('V: '+str(vGlob))

print('DATA:')
for i in range(0,len(data)):
    print(str(i)+': '+'; '.join(map(str, data[i])))
    
ga = pyeasyga.GeneticAlgorithm(data)

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
# and set the Genetic Algorithm's ``fitness_function`` attribute to
# your defined function
ga.fitness_function = fitness
ga.run()
print (ga.best_individual())
ans = ga.best_individual()
mass=0
V=0
cost=0
for (select, (profit)) in zip(ans[1], data):
        if select:
            mass += float(profit[0])
            V += float(profit[1])
            cost += float(profit[2])
            
print('Mass: '+str(massGlob))
print('V: '+str(vGlob))
print('Mass_ans: '+str(mass))
print('V_ans: '+str(V))
print('Cost_ans: '+str(cost))
