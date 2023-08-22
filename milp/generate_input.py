import numpy as np 
import sys
import random

class Vehicle:
    def __init__(self,ID,arrival_time,lane,number):
        self.ID = ID 
        self.arrival_time = arrival_time
        self.incLane = lane
        self.number = number

def nextTime(rateParameter):
    time = round(random.expovariate(rateParameter),2)
    return max(1,time)

def output(vehs):
    for i in range(len(vehs)):
        print(vehs[i].ID,vehs[i].arrival_time,vehs[i].incLane,vehs[i].number) 

def end_gen(last):
    for i in range (len(last)):
        if last[i] < int(sys.argv[3]):
            return 1
    return 0

lamb = float(sys.argv[1])
lanes = int(sys.argv[2])
vehs = []

last = [0] * lanes
nums = [0] * lanes
while(end_gen(last)):
    for i in range (lanes):
        id = sum(nums)
        arrival = last[i] + nextTime(lamb)
        last[i] = arrival
        if arrival <= int(sys.argv[3]):
            nums[i] += 1
            order = ord('A') + i
            vehs.append(Vehicle(chr(order) + "_" + str(nums[i]),arrival,chr(order),id))

        

    # if (num_A < veh_num):
    #     id = num_A + num_B
    #     arrival = lastA + nextTime(lamb)
    #     w_equal = random.choices(w,k=2 * veh_num)
    #     w_plus = random.choices(wp,k=2 * veh_num)
    #     for i in range (2 * veh_num):
    #         w_plus[i] = w_equal[i] + w_plus[i]
    #     for i in range(id):
    #         w_equal[i] = vehs[i].w_equal[id]
    #         w_plus[i] = vehs[i].w_plus[id]
    # vehs.append(Vehicle("A_" + str(num_A),arrival,'A',id,w_equal,w_plus))
    # lastA = arrival
    # num_A += 1







output(vehs)
        



    
