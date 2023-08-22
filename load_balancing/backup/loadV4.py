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
        self.w_equal = []
        self.w_plus = []
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

def Int2(lb,ub,name,veh_num):
    temp = []
    for i in range(veh_num):
        temp1 = []
        for j in range (veh_num):
            temp1.append(m.addVar(lb = lb, ub = ub,vtype=GRB.INTEGER,name=name + "_"  + str(i)+ "_"  + str(j)))
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

# A = []
# B = [Vehicle("B_1",1,'B',2),Vehicle("B_2",3,'B',4),Vehicle("B_3",4,'B',6)]

# A = [Vehicle("A_1",1,'A',1)]
# B = [Vehicle("B_1",1,'B',2),Vehicle("B_2",3,'B',4),Vehicle("B_3",4,'B',6),Vehicle("B_4",5,'B',8),Vehicle("B_5",8,'B',10),Vehicle("B_3",10,'B',7),Vehicle("B_4",12,'B',9),Vehicle("B_5",15,'B',11)]


A,B = deal_input(sys.argv[1])

W_init(A,B)
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
    T = 2
    e = Cont1("e",veh_num)
    e1 = Cont2("e1",veh_num)
    e2 = Cont2("e2",veh_num)
    # Integrate new variables
    m.update()

    o = Int1(0,N-1,"o",veh_num)
    l = Int1(0,M-1,"l",veh_num)
    t1 = Int1(-1,1,"t1",veh_num)
    t2 = Int1(0,1,"t2",veh_num)
    t3 = Binary2("t3",veh_num)
    t4 = Binary2("t4",veh_num)
    t5 = Int2(-1 * (M - 1),M-1,"t5",veh_num)
    t6 = Int2(0,M -1,"t6",veh_num)
    t7 = Int2(-1 * (N - 1),N-1,"t7",veh_num)
    t8 = Int2(0,N -1,"t8",veh_num)
    t = Binary2("t",veh_num)
    c = Binary1("c",veh_num)
    same = Binary2("same",veh_num)
    same_o = Binary2("same_o",veh_num)
    lo = Binary2("lo",veh_num)
    lo1 = Binary2("lo1",veh_num)




    for i in range (veh_num):
        m.addConstr(t1[i] == (l[i] - allVeh[i].incLane))
        m.addConstr(t2[i] == abs_(t1[i]))
        m.addConstr((c[i] == 0) >> (t2[i] == 0))
        m.addConstr((c[i] == 1) >> (t2[i] == 1))

    for i in range (veh_num):
        for j in range (veh_num):
            if i == j:
                continue
            if (abs(allVeh[i].arrival_time - allVeh[j].arrival_time) < T):
                m.addConstr(t3[i][j] == 0)
            else:
                m.addConstr(t3[i][j] == 1)
            m.addConstr(t5[i][j] == l[i] - l[j])
            m.addConstr(t6[i][j] == abs_(t5[i][j]))
            m.addConstr((same[i][j] == 1) >> (t6[i][j] == 0))
            m.addConstr((same[i][j] == 0) >> (t6[i][j] >= 1))
            m.addConstr(t7[i][j] == o[i] - o[j])
            m.addConstr(t8[i][j] == abs_(t7[i][j]))
            m.addConstr((same_o[i][j] == 1) >> (t8[i][j] == 0))
            m.addConstr((same_o[i][j] == 0) >> (t8[i][j] >= 1))
            
    for i in range (veh_num):
        for j in range (veh_num):
            if i == j:
                continue
            m.addConstr(t4[i][j] == or_(c[i],c[j]))

            ###model infeasible reason not found
            m.addConstr(t3[i][j] >= t4[i][j] * same[i][j])
    for i in range (veh_num):
        m.addConstr(e[i] >= allVeh[i].arrival_time + 50)
        for j in range (veh_num):
            if i == j:
                continue
            m.addConstr(e1[i][j] == e[i] - e[j])
            m.addConstr(e2[i][j] == abs_(e1[i][j]))
            if allVeh[i].arrival_time - allVeh[j].arrival_time > 0:
                m.addConstr((same[i][j] == 1) >> (e[i] - e[j] >= 2))
            else:
                m.addConstr((same[i][j] == 1) >> (e[j] - e[i] >= 2))
            m.addConstr(lo1[i][j] == 1-same[i][j])
            m.addConstr(lo[i][j] == and_(lo1[i][j],same_o[i][j]))
            m.addConstr((lo[i][j] == 0) >> (e2[i][j] >= 4))


    
            
                                
    b1 = Int1(-M,M,"b1",veh_num)
    b2 = Int1(0,M,"b2",veh_num)
    b3 = Binary1("b3",veh_num)
    b4 = Binary1("b4",veh_num)
    b5 = Binary1("b5",veh_num)
    b6 = Binary1("b6",veh_num)
    b7 = Binary1("b7",veh_num)
    b8 = Binary1("b8",veh_num)


    for i in range(veh_num):
        if M == N - 1:
            m.addConstr(0 >= l[i] - o[i])
            m.addConstr(-1 <= l[i] - o[i])
        if M == N - 2:
            middle = ceil(M/2)
            m.addConstr(b1[i] == l[i] - middle)
            m.addConstr(b2[i] == abs_(b1[i]))

            m.addConstr((b3[i]== 1) >> (b2[i]== 0))
            m.addConstr((b3[i]== 0) >> (b2[i]>= 1))
            m.addConstr((b4[i] == 1) >> (b1[i]<= -1))
            m.addConstr((b4[i]== 0) >> (b1[i]>= 0))
            m.addConstr((b5[i] == 1) >> (b1[i]>= 1))
            m.addConstr((b5[i] == 0) >> (b1[i]<= 0))
            m.addConstr(b8[i] == 1 - b3[i])
            m.addConstr(b6[i] == and_(b4[i],b8[i]))
            m.addConstr(b7[i] == and_(b5[i],b8[i]))

            m.addConstr((b3[i]== 1) >> (o[i] - l[i] >= 0))
            m.addConstr((b3[i]== 1) >> (o[i] - l[i] <= 2))
            m.addConstr((b6[i] == 1) >>(o[i] - l[i] >= 0))
            m.addConstr((b6[i] == 1) >>(o[i] - l[i] <= 1))
            m.addConstr((b7[i] == 1) >>( o[i] - l[i] >= 1))
            m.addConstr((b7[i] == 1) >> (o[i] - l[i] <= 2))
                

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
 
    fanjun = 0
    junfan = 0
    for i in range (N):
        fanjun += lane_veh[i] * lane_veh[i]
        junfan += lane_veh[i]
    fanjun /= N
    junfan = junfan *junfan / N / N

    
    # m.addConstr(l[0] == 0)
    # m.addConstr(l[1] == 1)



        
    # m.setObjective(u, GRB.MINIMIZE)   
    m
    maxtime = m.addVar(vtype=GRB.CONTINUOUS, name="maxtime")
    m.addConstr(maxtime == max_(e),name="maxconstr")
    m.setObjective(fanjun - junfan + maxtime * 0.001, GRB.MINIMIZE)
    m.optimize()
    m.write('mip1.lp')


    if m.status == GRB.INFEASIBLE:
        # Compute the infeasible constraints and print them
        m.computeIIS()
        print("The following constraints are infeasible:")
        for c in m.getConstrs():
            if c.IISConstr:
                print(c.constrName)
    for v in m.getVars():
        # if 'd_' in v.varName or 'e_' in v.varName or 'l_' in v.varName or 'o_' in v.varName or 'W_' in v.varName or 'p_' in v.varName:
        print('%s %g' % (v.varName, v.x))

    print('Obj: %g' % m.objVal)
    for i in allVeh:
        print(i.ID,i.arrival_time)

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
