import numpy as np
import random

class Vehicle:
    def __init__(self,ID,arrival_time,inlane,number,N):
        self.ID = ID 
        self.arrival_time = arrival_time
        self.position = arrival_time
        self.speed = 1
        self.incLane = ord(inlane) - ord('A')
        
        self.nextLane = -1
        self.outLane = -1
        self.leaveLane = -1
        self.number = number
        self.lane = [-1] * N

        self.decision_num = min(N-1,int(self.arrival_time // 15))
        
        self.expected_arrival = [-1] * N
        self.intersection_arrival = -1
        self.curr_expected_arrival = -1
        self.child_diff = 100
        self.curr_lane = -1
        self.decision_depart = [0] * (N + 1)
        self.scheduled_enter = -1
        self.ifChange = 0
        self.passingOrder = -1
        self.w_equal = []
        self.w_plus = []
        self.waiting = 0
        self.k = -1

def deal_input(N,infile):
    f = open(infile,"r")
    arr = []
    for i in range(N):
        arr.append([])
    temp_in = f.readline()
    while (len(temp_in) > 0):
        x = temp_in.split(" ")
        arr[ord(x[2]) - ord('A')].append(Vehicle(x[0],eval(x[1]),x[2],eval(x[3]),N))
        temp_in = f.readline()
    # for i in range(len(A)):
    #     print(A[i].ID,A[i].arrival_time,A[i].lane,A[i].number,A[i].w_equal,A[i].w_plus)
    return arr


def deal_waiting(allVeh):
    veh_num = len(allVeh)
    for i in range(veh_num):
        allVeh[i].w_equal = [-1] * veh_num
        allVeh[i].w_plus = [-1] * veh_num
    for i in range(veh_num):
        for j in range(veh_num):
            if i == j:
                continue
            if allVeh[j].w_equal[allVeh[i].number] == -1:
                temp = random.randint(2,4)
                allVeh[i].w_equal[allVeh[j].number] = temp
                allVeh[j].w_equal[allVeh[i].number] = temp 
                allVeh[i].w_plus[allVeh[j].number] = temp + 2
                allVeh[j].w_plus[allVeh[i].number] = temp + 2
    return allVeh

def deal_lane(allVeh,N,k):
    for j in range(len(allVeh)):
        allVeh[j].lane =[-1] * N
        if k == 0:
            inlane = allVeh[j].incLane
            for i in range (allVeh[j].decision_num + 1,0,-1):
                allVeh[j].lane[N - i] = (inlane)
                if allVeh[j].lane[N - i] < allVeh[j].outLane:
                    inlane += 1
                elif allVeh[j].lane[N - i] > allVeh[j].outLane:
                    inlane -= 1
        if k == 1:
            outlane = allVeh[j].outLane
            for i in range (allVeh[j].decision_num + 1,0,-1):
                allVeh[j].lane[N - i] = (outlane)
                if allVeh[j].lane[N - i] < allVeh[j].incLane:
                    outlane += 1
                elif allVeh[j].lane[N - i] > allVeh[j].incLane:
                    outlane -= 1
        
        allVeh[j].lane.reverse()
        allVeh[j].lane.append(-1)


    return allVeh
