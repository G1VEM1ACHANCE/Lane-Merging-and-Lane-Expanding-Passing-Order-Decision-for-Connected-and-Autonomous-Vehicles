from gurobipy import *
import sys
import numpy as np
from math import ceil
import random
class Vehicle:
    def __init__(self,ID,arrival_time,lane,number,w_equal,w_plus):
        self.ID = ID 
        self.arrival_time = arrival_time
        self.position = -1
        self.speed = 1
        if lane == 'A':
            self.incLane = 0
            self.lane = 0
        else:
            self.incLane = 1
            self.lane = 1
        self.number = number
        self.decision_arrive = -1
        self.decision_depart = -1
        self.scheduled_enter = -1
        self.ifChange = 0
        self.passingOrder = -1
        self.w_equal = w_equal
        self.w_plus = w_plus
        self.waiting = 0

def W_init(A,B):
    for i in range (len(A)):
        for j in range (len(A)):
            # if i == j:
            #     continue
            num = random.randint(1,5)
            A[i].w_equal.append(num)
            A[i].w_plus.append(num + 2)
        for j in range (len(B)):
            num = random.randint(1,5)
            A[i].w_equal.append(num)
            A[i].w_plus.append(num + 2)
    for i in range (len(B)):
        for j in range (len(A)):
            num = random.randint(1,5)
            B[i].w_equal.append(num)
            B[i].w_plus.append(num + 2)
        for j in range (len(B)):
            # if i == j:
            #     continue
            num = random.randint(1,5)
            B[i].w_equal.append(num)
            B[i].w_plus.append(num + 2)

def myFunc(e):
    return e.ID

def Binary1(name,veh_num):
    temp = []
    for i in range(veh_num):
        temp.append(m.addVar(vtype=GRB.BINARY,name= name + '_' +  str(i)))
    return temp

def Int1(lb,ub,name,veh_num):
    temp = []
    for i in range(veh_num):
        temp.append(m.addVar(lb = lb, ub = ub,vtype=GRB.INTEGER,name= name + "_" + str(i)))
    return temp


def Cont1(name,veh_num):
    temp = []
    for i in range(veh_num):
        temp.append(m.addVar(lb = 0, ub = 300, vtype=GRB.CONTINUOUS,name= name + "_" + str(i)))
    return temp

def Binary2(name,veh_num):
    temp = []
    for i in range(veh_num):
        temp1 = []
        for j in range (veh_num):
            temp1.append(m.addVar(vtype=GRB.BINARY,name=name + "_" + str(i) + "_"  + str(j)))
        temp.append(temp1)
    return temp

def Int2(name,veh_num):
    temp = []
    for i in range(veh_num):
        temp1 = []
        for j in range (veh_num):
            temp1.append(m.addVar(lb = -2, ub = 2,vtype=GRB.INTEGER,name=name + "_"  + str(i)+ "_"  + str(j)))
        temp.append(temp1)
    return temp

def Cont2(name,veh_num):
    temp = []
    for i in range(veh_num):
        temp1 = []
        for j in range (veh_num):
            temp1.append(m.addVar(lb = -300, ub = 300,vtype=GRB.CONTINUOUS,name= name + "_"  + str(i) + "_"  + str(j)))
        temp.append(temp1)
    return temp

def Binary3(name,veh_num):
    temp = []
    for i in range(veh_num):
        temp1 = []
        for j in range (veh_num):
            temp2 = []
            for k in range(veh_num):
                temp2.append(m.addVar(vtype=GRB.BINARY,name= name + "_" + str(i) + "_" + str(j) + "_" + str(k)))
            temp1.append(temp2)
        temp.append(temp1)
    return temp

def Cont3(name,veh_num):
    temp = []
    for i in range(veh_num):
        temp1 = []
        for j in range (veh_num):
            temp2 = []
            for k in range(veh_num):
                temp2.append(m.addVar(vtype=GRB.CONTINUOUS,name= name + "_" + str(i) + "_" + str(j) + "_" + str(k)))
            temp1.append(temp2)
        temp.append(temp1)
    return temp



def deal_input(infile):
    f = open(infile,"r")
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

# A = [Vehicle("A_1",1,'A',1),Vehicle("A_2",2,'A',3),Vehicle("A_3",3,'A',5),Vehicle("A_4",4,'A',7),Vehicle("A_5",16,'A',9)]
# B = [Vehicle("B_1",1,'B',2),Vehicle("B_2",3,'B',4),Vehicle("B_3",4,'B',6),Vehicle("B_4",5,'B',8)]

# A = [Vehicle("A_1",1,'A',1)]
# B = [Vehicle("B_1",1,'B',2),Vehicle("B_2",3,'B',4),Vehicle("B_3",4,'B',6),Vehicle("B_4",5,'B',8),Vehicle("B_5",8,'B',10)]

# W_init(A,B)
# print("aaaa")
# print(A[0].w_equal)
A,B = deal_input(sys.argv[1])
allVeh = A.copy() + B.copy()
allVeh.sort(key=myFunc)
veh_num = len(allVeh)

try:
    # Create a new model
    m = Model("mip1")
    m.setParam('Method', 0)
    decision_num = 1
    # Create variables
    M = 2
    N = 3
    # Integrate new variables
    m.update()

    o = Int1(0,N-1,"o",veh_num)
    c = Binary1("c",veh_num)

    for i in range(veh_num):
        if M == N - 1:
            m.addConstr(0 >= allVeh[i].incLane - o[i])
            m.addConstr(-1 <= allVeh[i].incLane - o[i])
        if M == N - 2:
            middle = ceil(M/2)
            if allVeh[i].incLane == middle:
                m.addConstr(o[i] - allVeh[i].incLane >= 0)
                m.addConstr(o[i] - allVeh[i].incLane <= 2)
            if allVeh[i].incLane < middle:
                m.addConstr(o[i] - allVeh[i].incLane >= 0)
                m.addConstr(o[i] - allVeh[i].incLane <= 1)
            if allVeh[i].incLane > middle:
                m.addConstr(o[i] - allVeh[i].incLane >= 1)
                m.addConstr(o[i] - allVeh[i].incLane <= 2)
                

    lane_veh = []

    for j in range (N):
        u = Binary1("u_" + str(j),veh_num)
        v2 = Int1(-N,N,"v2_" + str(j),veh_num)
        v3 = Int1(0,N,"v3_"+ str(j),veh_num)
        for i in range (veh_num):
            m.addConstr((v2[i] == o[i] - j))
            m.addConstr((v3[i] == abs_(v2[i])))
            m.addConstr((u[i] == 1) >> (v3[i] == 0))
            m.addConstr((u[i] == 0) >> (v3[i] >= 1))
        u1 = m.addVar(lb = 0,ub = 60,vtype=GRB.INTEGER,name="u1" + '_' + str(j))
        lane_veh.append(u1)
        m.addConstr(u1 == quicksum(u[i] for i in range (veh_num)))
        
    # m.addConstr(o[0] == 0)
    # m.addConstr(o[1] == 0)
    # m.addConstr(o[2] == 1)
    # m.addConstr(o[3] == 1)
    # m.addConstr(o[4] == 2)
    # m.addConstr(o[5] == 2)
    fanjun = 0
    junfan = 0
    for i in range (N):
        fanjun += lane_veh[i] * lane_veh[i]
        junfan += lane_veh[i]
    fanjun /= N
    junfan = junfan *junfan / N / N

    
    



        
    # m.setObjective(u, GRB.MINIMIZE)   
    m.setObjective(fanjun - junfan, GRB.MINIMIZE)       
    
    m.optimize()
    m.write('mip1.lp')

    for v in m.getVars():
        # if 'd_' in v.varName or 'e_' in v.varName or 'l_' in v.varName or 'o_' in v.varName or 'W_' in v.varName or 'p_' in v.varName:
        print('%s %g' % (v.varName, v.x))

    print('Obj: %g' % m.objVal)
    for i in allVeh:
        print(i.lane)

except GurobiError as err:
    # print the error message
    print('Error code ' + str(err.errno) + ": " + str(err))
    
    # compute the IIS
    m.computeIIS()
    m.write("model.ilp")
    
    # print the IIS constraints
    print('Constraints causing the error:')
    for c in m.getConstrs():
        if c.IISConstr:
            print(c.constrName)
