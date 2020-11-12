# -*- coding: utf-8 -*-
"""Untitled-Copy1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18kthosSPdXE9jd1rD6DFe8Te2o3sW7yR
"""

from igraph import *
from random import randint
import copy
from collections import Counter
from tqdm import tqdm
from multiprocessing import Process, Lock
import networkx as nx
import subprocess
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

def fix_partition(partition):
    check = [-1]*len(partition)
    cnt = -1
    for i in range(len(partition)):
        if partition[i] < i:
            if(check[i] > -1):
                for j in range(len(partition)):
                    if(check[j] == check[i] and j!=i and j!= partition[i]):
                        check[j] = check[partition[i]]
            check[i] = check[partition[i]]
        else:
            kk = i
            while(partition[kk] > kk):
                kk = partition[kk]
            if(check[kk] == -1):
                cnt += 1
                check[i] = cnt
                while(partition[i] > i):
                    check[partition[i]] = cnt
                    i = partition[i]
            else:
                check[i] = check[kk]
                while(partition[i] > i):
                    check[partition[i]] = check[kk]
                    i = partition[i]
    ch = [0]*len(partition)
    for i in range(len(partition)):
        ch[partition[i]] = 1
    cnt = 0
    for i in range(len(ch)):
        if ch[i]>0:
            ch[i] = cnt
            cnt += 1
    for i in range(len(partition)):
        partition[i] = ch[partition[i]]
    return partition, partition

def spart_fitness(graph, partition):
    partition, check = fix_partition(partition)
    snode = [0]*len(partition)
    comm = Counter(check)
    scom = [0]*len(comm)
    edges = 0
    scom_edges = [0]*len(comm)
    for i in range(len(partition)):
        k_in = 0
        k_out = 0
        for j in range(len(partition)):
            if graph[i,j] == 1:
                if check[i] == check[j]:
                    k_in += 1
                    scom_edges[check[i]] += 1
                    edges += 1
                else:
                    k_out += 1
                    edges += 1
        snode[i] = (k_in - k_out)/comm[check[i]]
        scom[check[i]] += (k_in+2)*snode[i]/2
    edges //= 2
    spart = 0
    for i in range(len(comm)):
        spart += (scom[i]*scom_edges[i])/(comm[i] * edges * 2)
    spart /= len(comm)
    return spart

def BWX(g, parent1, parent2, global_best, global_worst):
    child = []
    for i in range(len(parent1)):
        if(parent1[i] == global_best[i]):
            child.append(parent1[i])
        elif(parent1[i] == global_worst[i]):
            k = randint(0, len(parent1)-1)
            while(i!=k and g[i,k] == 0):
                k = randint(0, len(parent1)-1)
            child.append(k)
        else:
            child.append(parent2[i])
    return fix_partition(child)[1]

def mutation(g, parent):
    child = []
    for i in range(len(parent)):
        k = randint(0, len(parent)-1)
        while(i!=k and g[i,k] == 0):
            k = randint(0, len(parent)-1)
        child.append(k)
    return fix_partition(child)[1]

def spart(graph, num_nodes, lock):
    population_size = 500
    num_generations = 150
    elite = 10
    cluster = 50
    crossover = 80
    mutations = 50
    population = []
    for i in range(population_size):
        temp = []
        for i in range(num_nodes):
            k = randint(0, num_nodes-1)
            while(i!=k and graph[i,k] == 0):
                k = randint(0, num_nodes-1)
            temp.append(k)
        population.append(temp)
    arr = []
    for pop in population:
        arr.append((spart_fitness(graph, pop), pop))
    arr.sort(reverse=True)
    population = [y for (x,y) in arr]
    t = 0
    global_best = []
    for i in range(num_generations):
        n_population = []
        for i in range(population_size//elite):
            temp = [x for x in population[i]]
            n_population.append(temp)
        for i in range(population_size//elite, population_size):
            temp = [x for x in population[randint(0, population_size - 1)]]
            n_population.append(temp)
        arr = []
        for pop in n_population:
            arr.append((spart_fitness(graph, pop), pop))
        arr.sort(reverse=True)
        global_best = arr[0][1]
        global_worst = arr[-1][1]
        for i in range(population_size//elite, population_size):
            if randint(0, 99) < crossover:
                parent1 = n_population[i]
                x = []
                parent2 = []
                for j in range(cluster):
                    x.append(randint(0, population_size - 1))
                    x.sort()
                    parent2 = arr[x[0]][1]
                child = BWX(graph, parent1, parent2, global_best, global_worst)
                if spart_fitness(graph, child) > spart_fitness(graph, n_population[i]):
                    n_population[i] = child
            if randint(0, 99) < mutations:
                child = mutation(graph, n_population[i])
                if spart_fitness(graph, child) > spart_fitness(graph, n_population[i]):
                    n_population[i] = child
        population = copy.deepcopy(n_population)
    val = spart_fitness(graph, global_best)
    lock.acquire()
    f1 = open("temp.txt", "r")
    L = f1.readlines()
    f1.close()
    if float(L[0]) < val:
        f1 = open("temp.txt", "w")
        global_best = [str(x) for x in global_best]
        f1.writelines([str(val) + '\n', " ".join(global_best) + '\n'])
        f1.close()
    lock.release()

def spart_optimized(graph, num_nodes):
    f1 = open("temp.txt","w") 
    f1.writelines(["-123456\n","1 2 3 4 5 6\n"])
    f1.close()
    p = []
    lock = Lock()
    for i in range(80):
        p.append(Process(target=spart, args=(graph, num_nodes,lock,)))
    for i in range(len(p)):
        p[i].start()
    for i in range(len(p)):
        p[i].join()
    f1 = open("temp.txt","r") 
    L = f1.readlines()
    f1.close()
    return L[1]

# g = Graph([(0,1), (0,2), (1,2), (1,3), (1,4), (2,3), (2,4), (3,4)])

# spart_optimized(g, 5)

# " ".join(["3", "0", "2", "1"])

def clique(g, size, idx, num_nodes):
  for i in range(idx,num_nodes-1):
    for j in range(idx - size,idx):
      g[i,j] = 0

def Print(g,num_nodes):
  G = nx.Graph()
  for i in range(num_nodes):
    G.add_node(i)
  for i in range(num_nodes):
    for j in range(i+1, num_nodes):
      if g[i,j] == 1:
        G.add_edge(i,j)
  nx.draw(G, with_labels=True)

def hub_node(clq1, clq2, alpha, beta):
    num_nodes = 1 + clq1 + clq2
    g = Graph.Full(num_nodes)
    for i in range(1,clq1+1):
        for j in range(clq1+1, num_nodes):
            g[i,j] = 0
    for i in range(1, clq1-alpha+1):
        g[0,i] = 0
    for i in range(1, clq2-beta+1):
        g[0, clq1+i] = 0
    return spart_optimized(g, num_nodes)

x_start = 3
y_start = 3
x_end = 31
y_end = 31
x_val = [i for i in range(x_start, x_end)]
y_val = [i for i in range(y_start, y_end)]
x_y = [(x,y) for x in range(x_start, x_end) for y in range(y_start, y_end)]
matrix_ans = []
for x in range(x_start, x_end):
    matrix_ans.append([0 for y in range(y_start, y_end)])
for z in tqdm(range(len(x_y))):
    temp = 0
    part = hub_node(x_y[z][0], x_y[z][1], 2, 2)
    ch = {}
    for x in part:
        ch[x] = 1
    if part[0] in part[1:x_y[z][0]+1]:
        temp = 1
    elif part[0] in part[x_y[z][0] + 1:]:
        temp = 2
    elif len(ch) == 3:
        temp = 3
    else:
        temp = 0
    matrix_ans[z//(y_end - y_start)][z%(y_end - y_start)] = temp
print(matrix_ans)
plt.figure(figsize = (16,14))
sns.heatmap(matrix_ans,xticklabels=x_val, yticklabels=y_val)
plt.xlabel("right clique size")
plt.ylabel("left clique size")
plt.show()
store = []
for j in range(len(matrix_ans)):
    store.append(" ".join(str(matrix_ans[j][i]) for i in range(len(matrix_ans[0])))+'\n')
f1 = open("3-30-copy1.txt","w") 
f1.writelines(store)
f1.close()
