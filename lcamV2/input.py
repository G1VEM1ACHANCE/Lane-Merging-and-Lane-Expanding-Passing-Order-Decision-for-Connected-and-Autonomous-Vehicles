import numpy as np 
from test import Vehicle 
import random

def print_vehicles(A, B):
    print('A:')
    for i in range(len(A)):
        print('ID : ', A[i].ID) 
        print('arrival_time : ', A[i].arrival_time)
        #print('position : ', A[i].position)
        #print('speed : ', A[i].speed)
        print('incLane : ', A[i].incLane) 
        #print('lanes : ', A[i].lanes)
        #print('change_ind : ', A[i].change_ind)
        #print('cacc : ', A[i].cacc)
        #print('tp : ', A[i].tp)
        #print('tm : ', A[i].tm)

    print('B:')
    for i in range(len(B)):
        print('ID : ', B[i].ID) 
        print('arrival_time : ', B[i].arrival_time)
        #print('position : ', B[i].position)
        #print('speed : ', B[i].speed)
        print('incLane : ', B[i].incLane) 
        #print('lanes : ', B[i].lanes)
        #print('change_ind : ', B[i].change_ind)
        #print('cacc : ', B[i].cacc)
        #print('tp : ', B[i].tp)
        #print('tm : ', B[i].tm)

    

def get_arrival_time(Tsafe, used_table, max_arrival_time):
    pass

def getInput(Tsafe = 1, density = 8):    #同車道車arrival time保證不重複
    
    Na = random.randint(1,3)  #A車道車數
    Nb = random.randint(1,3)  #B車道車數
     
    max_arrival_time = max(Na, Nb) * (Tsafe + 10-density) #density為車道擁擠程度 1-10
    la = list(range(1,max_arrival_time+1))
    lb = list(range(1,max_arrival_time+1))
    random.shuffle(la)
    random.shuffle(lb)


    A = []
    B = []
    a = []    #arrival time for A
    b = []    #arrival time for B
    for i in range(Na):
        #print(la)
        a.append(la.pop())
        random.shuffle(la)
    a.sort()
    for i in range(Na):
        A.append(Vehicle("A_"+str(i+1), a[i],'A'))
    #print(a)

    for i in range(Nb):
        #print(lb)
        b.append(lb.pop())
        random.shuffle(lb)
    b.sort()
    for i in range(Nb):
        B.append(Vehicle("B_"+str(i+1), b[i],'B'))
    #print(b)
    print_vehicles(A,B)
    return A, B

def deal_input():
    f = open("./input/a","r")
    A = []
    B = []
    temp_in = f.readline()
    while (len(temp_in) > 0):
        x = temp_in.split("[")
        x1 = x[0].split(" ")
        x4 = x[1].split("]")
        x4 = x4[0].split(",")
        x4 = [eval(i) for i in x4]
        x5 = x[2].split("]")
        x5 = x5[0].split(",")
        x5 = [eval(i) for i in x5]
        if x1[2] == 'A':
            A.append(Vehicle(x1[0],eval(x1[1]),x1[2],eval(x1[3]),x4,x5))
        else:
            B.append(Vehicle(x1[0],eval(x1[1]),x1[2],eval(x1[3]),x4,x5))
        temp_in = f.readline()
    # for i in range(len(A)):
    #     print(A[i].ID,A[i].arrival_time,A[i].lane,A[i].number,A[i].w_equal,A[i].w_plus)
    return A,B
#getInput()







