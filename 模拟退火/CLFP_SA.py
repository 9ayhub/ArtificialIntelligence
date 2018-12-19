# coding:utf-8

import numpy as np
 
"旅行商问题 ( TSP , Traveling Salesman Problem )"
OpenCost = []
Open = [0,0,0,0,0,0,0,0,0,0]
Capacity = np.array([10, 10, 10, 10, 10, 10, 10, 10, 10, 10])
Demand = np.array([])
AssignCost = np.array([])
Assign = np.array([])


def initData():
  global coordinates
  fr = open('qa194.txt')
  for line in fr.readlines():
    lineArr = line.strip().split()
    temp = np.array([[float(lineArr[1]), float(lineArr[2])]])
    coordinates = np.vstack((coordinates, temp))
  fr.close()
  coordinates = coordinates[1:]
  print(coordinates.shape[0])

def getcost():
    cost = 0
    for i range(len(OpenCost)):
        cost += OpenCost[i] * Open[i]
    for i range(len(AssignCost)):
        for j range(len(AssignCost[0])):
            cost += AssignCost[i][j] * Assign[i][j]
    return cost

def exchange():
    while True:
        fac1 = np.int(np.ceil(np.random.rand()*(len(Open)-1)))
        fac2 = np.int(np.ceil(np.random.rand()*(len(Open)-1)))
        ## print(loc1,loc2)
        if Open[fac1] == 1 and Open[fac2] == 1 and  fac1 != fac2:
            break
    while True:
        cus1 = np.int(np.ceil(np.random.rand()*(len(Assign)-1)))
        cus2 = np.int(np.ceil(np.random.rand()*(len(Assign)-1)))
        ## print(loc1,loc2)
        if Assign[fac1][cus1] == 1 and Assign[fac2][cus2] == 1:
            break
    

def initpara():
    alpha = 0.999
    t = (1,100)
    markovlen = 1000
 
    return alpha,t,markovlen

initData()
num = coordinates.shape[0]
distmat = getdistmat(coordinates) #得到距离矩阵
 
 
solutionnew = np.arange(num)
#valuenew = np.max(num)
 
solutioncurrent = solutionnew.copy()
valuecurrent =99000  #np.max这样的源代码可能同样是因为版本问题被当做函数不能正确使用，应取一个较大值作为初始值
#print(valuecurrent)
 
solutionbest = solutionnew.copy()
valuebest = 99000 #np.max
 
alpha,t2,markovlen = initpara()
t = t2[1]
 
result = [] #记录迭代过程中的最优解
while t > t2[0]:
    for i in np.arange(markovlen):
 
        #下面的两交换和三角换是两种扰动方式，用于产生新解
        if np.random.rand() > 0.5:# 交换路径中的这2个节点的顺序
            # np.random.rand()产生[0, 1)区间的均匀随机数
            while True:#产生两个不同的随机数
                loc1 = np.int(np.ceil(np.random.rand()*(num-1)))
                loc2 = np.int(np.ceil(np.random.rand()*(num-1)))
                ## print(loc1,loc2)
                if loc1 != loc2:
                    break
            solutionnew[loc1],solutionnew[loc2] = solutionnew[loc2],solutionnew[loc1]
        else: #三交换
            while True:
                loc1 = np.int(np.ceil(np.random.rand()*(num-1)))
                loc2 = np.int(np.ceil(np.random.rand()*(num-1))) 
                loc3 = np.int(np.ceil(np.random.rand()*(num-1)))
 
                if((loc1 != loc2)&(loc2 != loc3)&(loc1 != loc3)):
                    break
 
            # 下面的三个判断语句使得loc1<loc2<loc3
            if loc1 > loc2:
                loc1,loc2 = loc2,loc1
            if loc2 > loc3:
                loc2,loc3 = loc3,loc2
            if loc1 > loc2:
                loc1,loc2 = loc2,loc1
 
            #下面的三行代码将[loc1,loc2)区间的数据插入到loc3之后
            tmplist = solutionnew[loc1:loc2].copy()
            solutionnew[loc1:loc3-loc2+1+loc1] = solutionnew[loc2:loc3+1].copy()
            solutionnew[loc3-loc2+1+loc1:loc3+1] = tmplist.copy()  
 
        valuenew = 0
        for i in range(num-1):
            valuenew += distmat[solutionnew[i]][solutionnew[i+1]]
        valuenew += distmat[solutionnew[0]][solutionnew[193]]
       # print (valuenew)
        if valuenew<valuecurrent: #接受该解
           
            #更新solutioncurrent 和solutionbest
            valuecurrent = valuenew
            solutioncurrent = solutionnew.copy()
 
            if valuenew < valuebest:
                valuebest = valuenew
                solutionbest = solutionnew.copy()
        else:#按一定的概率接受该解
            if np.random.rand() < np.exp(-(valuenew-valuecurrent)/t):
                valuecurrent = valuenew
                solutioncurrent = solutionnew.copy()
            else:
                solutionnew = solutioncurrent.copy()
    t = alpha*t
    result.append(valuebest)
    show_path(solutionbest, valuebest, t)


