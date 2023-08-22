from gurobipy import *
import sys
import numpy as np
import random
from statistics import mean
class Vehicle:
    def __init__(self,ID,arrival_time,inlane,outlane,leavelane,number):
        N = 3
        self.ID = ID 
        self.arrival_time = arrival_time + 15
        self.position = arrival_time + 15
        self.speed = 1
        self.incLane = inlane
        
        self.nextLane = -1
        self.outLane = outlane
        self.leaveLane = leavelane
        self.number = number
        self.lane = [-1] * N

        self.decision_num = min(N-1,int(self.arrival_time // 15))
        for i in range (self.decision_num + 1,0,-1):
            self.lane[N - i] = (outlane)
            if self.lane[N - i] < self.incLane:
                outlane += 1
            elif self.lane[N - i] > self.incLane:
                outlane -= 1
        self.expected_arrival = [-1] * N
        self.curr_expected_arrival = -1
        self.lane.append(-1)
        self.decision_depart = [0] * (N + 1)
        self.scheduled_enter = -1
        self.ifChange = 0
        self.passingOrder = -1
        self.w_equal = 2
        self.w_plus = 5
        self.waiting = 0

# def W_init(allVeh):
#     for i in range (len(allVeh)):
#         for j in range (len(allVeh)):
#             if i == j:
#                 allVeh[i].w_equal.append((allVeh[j].ID,0))
#                 allVeh[i].w_plus.append((allVeh[j].ID,0))
#                 continue
#             num = 2
#             allVeh[i].w_equal.append((allVeh[j].ID,num))
#             allVeh[i].w_plus.append((allVeh[j].ID,num + 2))
#     return allVeh

def myFunc(e):
    return e.arrival_time

def myFunc1(e):
    return e.curr_expected_arrival



def deal_input(M,infile):
    f = open(infile,"r")
    arr = []
    temp_in = f.readline()
    while (len(temp_in) > 0):
        x = temp_in.split(" ")
        arr.append(Vehicle(x[0],eval(x[1]),eval(x[2]),eval(x[3]),eval(x[4]),eval(x[5])))
        temp_in = f.readline()
    # for i in range(len(A)):
    #     print(A[i].ID,A[i].arrival_time,A[i].lane,A[i].number,A[i].w_equal,A[i].w_plus)
    return arr

# def deal_lane(allVeh,veh_num):
    

def deal_predecision(allVeh,veh_num):
    for i in range (veh_num):
        if allVeh[i].position % 15 < 3 and allVeh[i].position % 15 >= 2:
            allVeh[i].speed =  allVeh[i].position % 15 - 2

def assign_passing(allVeh,veh_num,n):
    for i in range (veh_num):
        if allVeh[i].decision_num == n + 1:
            allVeh[i].expected_arrival[n] = allVeh[i].arrival_time - 15 * (n + 1)
        elif allVeh[i].decision_num > n + 1:
            allVeh[i].expected_arrival[n] = allVeh[i].decision_depart[n + 1] + 15
        allVeh[i].curr_expected_arrival = allVeh[i].expected_arrival[n]
    allVeh.sort(key=myFunc1)
    for i in range(veh_num):
        allVeh[i].passingOrder = i
    return allVeh
    
    



            


def findmaxpred(veh,allVeh,veh_num,n,N):
    time = [0]
    for i in range (veh_num):
        # if allVeh[veh].ID == "A_2" and allVeh[i].ID == "B_1":
        #     print(allVeh[veh].ID,allVeh[i].ID,allVeh[i].lane[n] , allVeh[veh].lane[n])
        #     print(allVeh[i].decision_depart[n])
        if allVeh[i].passingOrder < allVeh[veh].passingOrder and allVeh[i].lane[n] == allVeh[veh].lane[n]:
            if allVeh[i].lane[n + 1] == allVeh[veh].lane[n + 1] and allVeh[i].lane[n] == allVeh[i].lane[n+1]:
                time.append(allVeh[i].decision_depart[n] + 1)
            else:
                time.append(allVeh[i].decision_depart[n] + 4)
        
        if allVeh[i].passingOrder < allVeh[veh].passingOrder and allVeh[i].lane[n] == allVeh[veh].lane[n + 1] and allVeh[veh].lane[n] != allVeh[veh].lane[n+1]:
            time.append(allVeh[i].decision_depart[n] + 4)
        elif allVeh[i].passingOrder < allVeh[veh].passingOrder and allVeh[veh].lane[n] == allVeh[i].lane[n + 1] and allVeh[veh].lane[n] != allVeh[i].lane[n]:
            time.append(allVeh[i].decision_depart[n] + 1)
    maxtime = max(time)


    if allVeh[veh].position >= (n + 1) * 15 and allVeh[veh].position < (n + 2) * 15:
        allVeh[veh].decision_depart[n] = max(maxtime, allVeh[veh].position - (n + 1) * 15)
    elif n < 3:
        allVeh[veh].decision_depart[n] = max(maxtime , allVeh[veh].decision_depart[n + 1] +  15)
    if allVeh[veh].position < (n + 1) * 15 :
        allVeh[veh].decision_depart[n] = 0 
    else:
        if maxtime == 0 and allVeh[veh].decision_depart[n+1] == 0:
            allVeh[veh].decision_depart[n] = allVeh[veh].position - (n + 1) * 15
    if n == N - 2 and allVeh[veh].arrival_time > (n + 1) * 15:
        allVeh[veh].decision_depart[n] = max(allVeh[veh].position - (n + 1) * 15,allVeh[veh].decision_depart[n])
    return allVeh
def myFunc3(e):
    return e.passingOrder

def deal_enter(veh,allVeh,veh_num):
    time = [0]
    same = 0
    diff = 0
    allVeh.sort(key=myFunc3)
    for i in range (veh - 1,0,-1):
        if allVeh[i].outLane == allVeh[veh].outLane:
            same = i
            time.append(allVeh[i].scheduled_enter + allVeh[i].w_equal[allVeh[veh].number])
            break
    for i in range (veh - 1,0,-1):
        if allVeh[i].leaveLane == allVeh[veh].leaveLane:
            diff = i
            break
    if same != diff:
        time.append(allVeh[i].scheduled_enter + allVeh[diff].w_plus[allVeh[veh].number])
            

    if allVeh[veh].decision_depart[0] == 0:
        allVeh[veh].scheduled_enter = max(max(time),allVeh[veh].arrival_time)
    else:
        allVeh[veh].scheduled_enter = max(max(time),allVeh[veh].decision_depart[0] + 15)
    return allVeh

        
            

            


def schedule_enter(allVeh,N):
    allVeh.sort(key=myFunc)
    veh_num = len(allVeh)
    for i in range (veh_num):
        allVeh[i].passingOrder = i
    for j in range(1,N):
        allVeh = assign_passing(allVeh,veh_num,N - 1 - j)
        for i in range(veh_num):
            allVeh = findmaxpred(i,allVeh,veh_num, N - 1 - j,N)
    for i in range(veh_num):
        allVeh = deal_enter(i,allVeh,veh_num)
    schedule = []
    delay = []
    for i in range(veh_num):
        # print(allVeh[i].ID,allVeh[i].lane,allVeh[i].outLane,allVeh[i].leaveLane,allVeh[i].decision_num,allVeh[i].decision_depart,allVeh[i].scheduled_enter)
        delay.append(- allVeh[i].arrival_time + allVeh[i].scheduled_enter)
        schedule.append(allVeh[i].scheduled_enter)
    # print("max =", max(delay))
    return allVeh,max(delay),mean(delay),max(schedule)


        
    
    



# A = [Vehicle("A_1",1,0,2,1,1),Vehicle("A_2",2,0,0,0,2),Vehicle("A_3",3,0,0,1,3),Vehicle("A_4",4,0,0,0,4),Vehicle("A_5",16,0,2,2,5)]
# B = [Vehicle("B_1",1,1,1,1,6),Vehicle("B_2",3,1,1,1,7),Vehicle("B_3",4,1,1,1,8),Vehicle("B_4",5,1,1,1,9),Vehicle("B_5",15,1,1,2,10)]
# C = [Vehicle("C_1",1,2,2,2,11),Vehicle("C_2",3,2,2,2,12),Vehicle("C_3",4,2,2,2,13),Vehicle("C_4",5,2,2,2,14),Vehicle("C_5",15,2,1,2,15)]

# A = [Vehicle("A_1",16,0,2,3,1),Vehicle("A_2",17,0,1,0,2)]
# B = [Vehicle("B_1",16,1,1,1,6),Vehicle("B_2",17,1,1,1,7)]
# C = [Vehicle("C_1",16,2,2,2,11),Vehicle("C_2",17,2,1,2,12)]
# # allVeh = deal_input(4,sys.argv[1])
# allVeh = A + B + C
# # allVeh = W_init(allVeh)
# veh_num = len(allVeh)
# schedule_enter(allVeh,3)