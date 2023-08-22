import loadV7
import input,FCFS,scheduleV4,heuristic
import sys
from gurobipy import *
import random
from verify import verify
import numpy as np
import time
from statistics import mean

M = eval(sys.argv[2])
N = eval(sys.argv[3])
arr = input.deal_input(M,sys.argv[1])
allVeh = []
for i in range(M):
    allVeh += arr[i]
allVeh = input.deal_waiting(allVeh)

# for i in range (len(allVeh)):
#     print(allVeh[i].ID,allVeh[i].number,allVeh[i].w_equal,allVeh[i].w_plus)

temp = allVeh.copy()
solut_val = []
V3 = []
V4 = []
V6 = []
V31 = []
V41 = []
V61 = []
V32 = []
V42 = []
V62 = []
milp_time = []
V3_time = []
V6_time = []
for i in range (30):
    start = time.time()
    allVeh = temp.copy()
    m = Model("mip1")
    m.setParam('Method', 0)
    m.params.NonConvex = 2
    random.shuffle(allVeh)
    allVeh = loadV7.milp1(m,M,N,allVeh)
    allVeh = loadV7.model_solution(m,allVeh)
    end = time.time()
    milp_time.append(end - start)
    temp1 = allVeh.copy()
    # for i in range (len(allVeh)):
    #     print(allVeh[i].ID,allVeh[i].lane)
    
    allVeh = input.deal_lane(allVeh,M,0)
    start = time.time()
    allVeh,maxval,meanval,maxsched = FCFS.schedule_enter(allVeh,M)
    end = time.time()
    V3_time.append(end - start)
    V3.append(maxval)
    V31.append(meanval)
    V32.append(maxsched)
    print("FCFS",maxval,meanval,maxsched,end-start)

    allVeh = temp1.copy()
    allVeh = input.deal_lane(allVeh,M,1)
    allVeh,maxval,meanval,maxsched = scheduleV4.schedule_enter(allVeh,M)
    V4.append(maxval)
    V41.append(meanval)
    V42.append(maxsched)


    allVeh = temp1.copy()
    allVeh = input.deal_lane(allVeh,M,0)
    start = time.time()
    allVeh,maxval,meanval,maxsched = heuristic.schedule_enter(allVeh,M)
    end = time.time()
    V6_time.append(end - start)
    V6.append(maxval)
    V61.append(meanval)
    V62.append(maxsched)
    

    # verify(allVeh)

    
print("min",min(V3),min(V4),min(V6),min(V31),min(V41),min(V61),min(V32),min(V42),min(V62),mean(milp_time),mean(V3_time),mean(V6_time))


