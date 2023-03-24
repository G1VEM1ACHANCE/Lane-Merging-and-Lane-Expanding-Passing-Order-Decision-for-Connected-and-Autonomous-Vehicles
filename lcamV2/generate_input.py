import numpy as np 
import sys
import random

class Vehicle:
    def __init__(self,ID,arrival_time,lane,number,w_equal,w_plus):
        self.ID = ID 
        self.arrival_time = arrival_time
        self.incLane = lane
        self.number = number
        self.w_plus = w_plus
        self.w_equal = w_equal

def nextTime(rateParameter):
    time = round(random.expovariate(rateParameter),2)
    return max(1,time)

def output(vehs):
    for i in range(len(vehs)):
        print(vehs[i].ID,vehs[i].arrival_time,vehs[i].incLane,vehs[i].number,vehs[i].w_equal,vehs[i].w_plus) 

lamb = float(sys.argv[1])
veh_num = int(sys.argv[2])
vehs = []
num_A = 0
num_B = 0
t = 0
w = [1,2,3,4,5,6]
wp = [0,1,2]
lastA = 0
lastB = 0
for i in range (veh_num):
    if (num_A < veh_num):
        id = num_A + num_B
        arrival = lastA + nextTime(lamb)
        w_equal = random.choices(w,k=2 * veh_num)
        w_plus = random.choices(wp,k=2 * veh_num)
        for i in range (2 * veh_num):
            w_plus[i] = w_equal[i] + w_plus[i]
        for i in range(id):
            w_equal[i] = vehs[i].w_equal[id]
            w_plus[i] = vehs[i].w_plus[id]
    vehs.append(Vehicle("A_" + str(num_A),arrival,'A',id,w_equal,w_plus))
    lastA = arrival
    num_A += 1

for i in range (veh_num):
    if (num_B < veh_num):
        id = num_A + num_B
        arrival = lastB + nextTime(lamb)
        w_equal = random.choices(w,k=2 * veh_num)
        w_plus = random.choices(wp,k=2 * veh_num)
        for i in range (2 * veh_num):
            w_plus[i] = w_equal[i] + w_plus[i]
        for i in range(id):
            w_equal[i] = vehs[i].w_equal[id]
            w_plus[i] = vehs[i].w_plus[id]
    vehs.append(Vehicle("B_" + str(num_B),arrival,'B',id,w_equal,w_plus))
    lastB = arrival
    num_B += 1

# while (num_A < veh_num or num_B < veh_num):
#     if num_A < veh_num:
#         id = num_A + num_B
#         w_equal = random.choices(w,k=2 * veh_num)
#         w_plus = random.choices(wp,k=2 * veh_num)
#         for i in range (2 * veh_num):
#             w_plus[i] = w_equal[i] + w_plus[i]
#         for i in range(id):
#             w_equal[i] = vehs[i].w_equal[id]
#             w_plus[i] = vehs[i].w_plus[id]
#         w_equal[id] = 0
#         w_plus[id] = 0
#         vehs.append(Vehicle("A_" + str(num_A),t,'A',id,w_equal,w_plus))
#         num_A += 1
#     if num_B < veh_num and random.uniform(0,1) < lamb:
#         id = num_A + num_B
#         w_equal = random.choices(w,k=2 * veh_num)
#         w_plus = random.choices(wp,k=2 * veh_num)
#         for i in range (2 * veh_num):
#             w_plus[i] = w_equal[i] + w_plus[i]
#         for i in range(id):
#             w_equal[i] = vehs[i].w_equal[id]
#             w_plus[i] = vehs[i].w_plus[id]
#         w_equal[id] = 0
#         w_plus[id] = 0
#         vehs.append(Vehicle("B_" + str(num_B),t,'B',id,w_equal,w_plus))
#         num_B += 1
#     t += 1
output(vehs)
        



    
