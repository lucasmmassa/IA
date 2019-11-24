import requests as rq
import numpy as np
import json
import random

url = 'http://localhost:8080/antenna/simulate'
url2 = 'https://aydanomachado.com/mlclass/02_Optimization.php'
low = 0
high = 360
individuals = 20
genes = 6
mphi1 = 0
mtheta1 = 0
mphi2 = 0
mtheta2 = 0
mphi3 = 0
mtheta3 = 0
mgain = -9999

def initialize(population):
    for i in range(20):
        population[i][0] = random.randint(0,360)
        population[i][1] = random.randint(0,360)
        population[i][2] = random.randint(0,360)
        population[i][3] = random.randint(0,360)
        population[i][4] = random.randint(0,360)
        population[i][5] = random.randint(0,360)
    return population

def getResult(phi1, theta1, phi2, theta2, phi3, theta3):
    angles = {'phi1':str(phi1), 'theta1':str(theta1), 'phi2':str(phi2), 'theta2':str(theta2), 'phi3':str(phi3), 'theta3':str(theta3), 'dev_key':'Lone Wolf'}
    result = rq.get(url2, params = angles)
    result = float(json.loads(result.content)['gain'])
    return result

def getFitness(population):
    fitness = [0]*20
    global mphi1 
    global mtheta1 
    global mphi2 
    global mtheta2 
    global mphi3 
    global mtheta3 
    global mgain 
    for i in range(individuals):
        result = getResult(population[i][0],population[i][1],population[i][2],population[i][3],population[i][4],population[i][5])
        fitness[i] = result
        if(result>mgain):            
            mphi1 = population[i][0]
            mtheta1 = population[i][1]
            mphi2 = population[i][2]
            mtheta2 = population[i][3]
            mphi3 = population[i][4]
            mtheta3 = population[i][5]
            mgain = result

    return fitness

def getParents(population,fitness,n):
    counter = 0
    parents = np.empty(shape=(n,6),dtype=int)
    for i in range(n):
        max = float(fitness[0])
        index = 0
        for f in range(len(fitness)):
            value = float(fitness[f])
            if(value > max):
                index = f
                max = fitness[f]
        parents[counter] = population[index]
        fitness = np.delete(fitness,index)
        population = np.delete(population,index,axis=0)
        counter = counter+1
    return parents

def crossover(parents,n):
    children = np.empty(shape=(20,6),dtype=int)
    for i in range(20):
        k = random.randint(1,4)
        p = random.randint(0,n-1)
        children[i][:k] = parents[p][:k]
        p = random.randint(0,100)
        p = p%n
        children[i][k:] = parents[p][k:]
    return children

def mutation(children,m):
    for count in range(m):
        i = random.randint(0,19)
        j = random.randint(0,5)
        #k = random.randint(0,359)
        #children[i][j] = k
        if(j==0):
            children[i][0] = random.randint(0,359)
        elif(j==1):
            children[i][1] = random.randint(0,359)
        elif(j==2):
            children[i][2] = random.randint(0,359)
        elif(j==3):
            children[i][3] = random.randint(0,359)
        elif(j==4):
            children[i][4] = random.randint(0,359)
        elif(j==5):
            children[i][5] = random.randint(0,359)
            
    return children

def newPopulation(parents,children):
    new = np.empty(shape=(20,6),dtype=int)
    new[18] = parents[0]
    new[19] = parents[1]
    fit = getFitness(children)
    print(fit,'\n')
    counter = 0
    for i in range(18):
        max = float(fit[0])
        index = 0
        for f in range(len(fit)):
            value = float(fit[f])
            if(value > max):
                index = f
                max = fit[f]
        new[counter] = children[index]
        fit = np.delete(fit,index)
        children = np.delete(children,index,axis=0)
        counter = counter+1
    return new

populationSize = (individuals,genes)

population = np.random.randint(low = low, high = high, size = populationSize)
population = initialize(population)

generations = 200

for g in range(generations):
    print('##')
    fitness = getFitness(population)
    print(fitness,'\n')

    n = 16

    parents = getParents(population,fitness,n)

    children = crossover(parents,n)

    m = 12

    children = mutation(children,m)

    population = newPopulation(parents,children)

    print('max: ',mgain,' - angles - ',mphi1,' ',mtheta1,' ',mphi2,' ',mtheta2,' ',mphi3,' ',mtheta3,'\n')
