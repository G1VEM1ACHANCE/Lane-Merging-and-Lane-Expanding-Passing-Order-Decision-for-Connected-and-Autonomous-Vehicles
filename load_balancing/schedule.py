from gurobipy import *
import sys
import numpy as np
import random
class Vehicle:
    def __init__(self,ID,arrival_time,inlane,outlane,leavelane,number):
        N = 3
        self.ID = ID 
        self.arrival_time = arrival_time
        self.position = -1
        self.speed = 1
        self.incLane = inlane
        self.outLane = outlane
        self.leaveLane = leavelane
        self.number = number

        self.decision_num = int(max(N - 1 - ((arrival_time)// 15),0))
        self.decision_depart = -1
        self.scheduled_enter = -1
        self.ifChange = 0
        self.passingOrder = -1
        self.w_equal = []
        self.w_plus = []
        self.waiting = 0

def W_init(allVeh):
    for i in range (len(allVeh)):
        for j in range (len(allVeh)):
            if i == j:
                allVeh[i].w_equal.append((allVeh[j].ID,0))
                allVeh[i].w_plus.append((allVeh[j].ID,0))
                continue
            num = 2
            allVeh[i].w_equal.append((allVeh[j].ID,num))
            allVeh[i].w_plus.append((allVeh[j].ID,num + 2))
    return allVeh

def myFunc(e):
    return e.number

def Binary1(name,veh_num):
    temp = []
    for i in range(veh_num):
        temp.append(m.addVar(vtype=GRB.BINARY,name= name + str(i)))
    return temp

def Int1(name,veh_num):
    temp = []
    for i in range(veh_num):
        temp.append(m.addVar(lb = -1, ub = 1,vtype=GRB.INTEGER,name= name + "_" + str(i)))
    return temp


def Cont1(name,veh_num):
    temp = []
    for i in range(veh_num):
        temp.append(m.addVar(lb = 0, ub = 300, vtype=GRB.CONTINUOUS,name= name + "_" + str(i)))
    return temp

def Binary2(name,mm,n):
    temp = []
    for i in range(mm):
        temp1 = []
        for j in range (n):
            temp1.append(m.addVar(vtype=GRB.BINARY,name=name + "_" + str(i) + "_"  + str(j)))
        temp.append(temp1)
    return temp

def Int2(lb,ub,name,mm,n):
    temp = []
    for i in range(mm):
        temp1 = []
        for j in range (n):
            temp1.append(m.addVar(lb = lb, ub = ub,vtype=GRB.INTEGER,name=name + "_"  + str(i)+ "_"  + str(j)))
        temp.append(temp1)
    return temp

def Cont2(lb,ub,name,mm,n):
    temp = []
    for i in range(mm):
        temp1 = []
        for j in range (n):
            temp1.append(m.addVar(lb = lb, ub = ub,vtype=GRB.CONTINUOUS,name= name + "_"  + str(i) + "_"  + str(j)))
        temp.append(temp1)
    return temp

def Binary3(name,veh_num,n):
    temp = []
    for i in range(veh_num):
        temp1 = []
        for j in range (veh_num):
            temp2 = []
            for k in range(n):
                temp2.append(m.addVar(vtype=GRB.BINARY,name= name + "_" + str(i) + "_" + str(j) + "_" + str(k)))
            temp1.append(temp2)
        temp.append(temp1)
    return temp

def Cont3(lb,ub,name,veh_num,n):
    temp = []
    for i in range(veh_num):
        temp1 = []
        for j in range (veh_num):
            temp2 = []
            for k in range(n):
                temp2.append(m.addVar(lb=lb,ub=ub,vtype=GRB.CONTINUOUS,name= name + "_" + str(i) + "_" + str(j) + "_" + str(k)))
            temp1.append(temp2)
        temp.append(temp1)
    return temp

def Int3(lb,ub,name,veh_num,n):
    temp = []
    for i in range(veh_num):
        temp1 = []
        for j in range (veh_num):
            temp2 = []
            for k in range(n):
                temp2.append(m.addVar(lb=lb,ub=ub,vtype=GRB.INTEGER,name= name + "_" + str(i) + "_" + str(j) + "_" + str(k)))
            temp1.append(temp2)
        temp.append(temp1)
    return temp



def deal_input(M,infile):
    f = open(infile,"r")
    arr = []
    temp_in = f.readline()
    while (len(temp_in) > 0):
        x = temp_in.split(" ")
        print(x)
        arr.append(Vehicle(x[0],eval(x[1]),eval(x[2]),eval(x[3]),eval(x[4]),eval(x[5])))
        temp_in = f.readline()
    # for i in range(len(A)):
    #     print(A[i].ID,A[i].arrival_time,A[i].lane,A[i].number,A[i].w_equal,A[i].w_plus)
    return arr



def milp(allVeh,M,N):
    try:
        # Create a new model
        m.setParam('Method', 0)
        # Create variables
        veh_num = len(allVeh)

        e = Cont1("e",veh_num)
        e1 = Cont1("e1",veh_num)
        d_prime = Cont2(0,300,"d_p",veh_num,N)
        d = Cont2(0,300,"d",veh_num,N)
        l = Int2(0,M - 1,"l",veh_num,N)
        l1 = Int2(- M + 1,M - 1,"l1",veh_num,N)
        l2 = Int2(0,1,"l2",veh_num,N)
        c = Binary2("c",veh_num,N)
        c1 = Binary3("c1",veh_num,N)
        c2 = Binary3("c2",veh_num,N)
        c3 = Binary3("c3",veh_num,N)
        c4 = Binary3("c4",veh_num,N)
        l3 = Int3(- M + 1,M - 1,"l3",veh_num,N)
        l4 = Int3(0,M - 1,"l4",veh_num,N)
        l5 = Int3(- M + 1,M - 1,"l5",veh_num,N)
        l6 = Int3(0,M - 1,"l6",veh_num,N)
        d1 = Cont3(-300,300,"d1",veh_num,N)
        d2 = Cont3(0,300,"d2",veh_num,N)
        d3 = Binary3("d3",veh_num,N)
        d4 = Binary3("d4",veh_num,N)





        maxtime = m.addVar(vtype=GRB.CONTINUOUS, name="maxtime")
        
    
        
        # Integrate new variables
        m.update()

        for i in range(veh_num):
            m.addConstr(e[i] >= d_prime[i][N-2] + min(15,allVeh[i].arrival_time), "earliest_enter")
            for j in range (allVeh[i].decision_num,N-1):
                m.addConstr(d_prime[i][j] >= d[i][j])
                if j >= allVeh[i].decision_num + 1:
                    m.addConstr(d_prime[i][j] >= d_prime[i][j-1] + 15)
                else:
                    # print(allVeh[i].arrival_time - 15 * (N - 1 - j),j)
                    m.addConstr(d_prime[i][j] >= allVeh[i].arrival_time - 15 * (N - 1 - j),"decision_constr2")
            if allVeh[i].decision_num == N-1:
                m.addConstr(d_prime[i][N-1] >= allVeh[i].arrival_time ,"decision_constr2")
        
        

        for i in range (veh_num):
            # print(allVeh[i].decision_num,allVeh[i].outLane,allVeh[i].incLane)
            m.addConstr(l[i][N-1] == allVeh[i].outLane)
            m.addConstr(l[i][allVeh[i].decision_num] == allVeh[i].incLane)
            for j in range (allVeh[i].decision_num + 1,N):
                m.addConstr(l1[i][j] == l[i][j] - l[i][j - 1])
                m.addConstr(l2[i][j] == abs_(l1[i][j]))
                m.addConstr(l2[i][j] <= 1)
                m.addConstr((c[i][j-1] == 1) >> (l2[i][j] >= 1))
                m.addConstr((c[i][j-1] == 0) >> (l2[i][j] == 0))

        
        for i in range (veh_num):
            for j in range(veh_num):
                if i == j:
                    continue
                for k in range (N):
                    m.addConstr(l3[i][j][k] == l[i][k] - l[j][k])
                    m.addConstr(l4[i][j][k] == abs_(l3[i][j][k]))
                    m.addConstr((c1[i][j][k] == 1) >> (l4[i][j][k] == 0))
                    m.addConstr((c1[i][j][k] == 0) >> (l4[i][j][k] >= 1))
                    if k >= 1:
                        m.addConstr(l5[i][j][k] == l[i][k] - l[j][k-1])
                        m.addConstr(l6[i][j][k] == abs_(l5[i][j][k]))
                        m.addConstr((c2[i][j][k] == 1) >> (l6[i][j][k] == 0))
                        m.addConstr((c2[i][j][k] == 0) >> (l6[i][j][k] >= 1))
                    m.addConstr(d1[i][j][k] == d_prime[i][k] - d_prime[j][k])
                    m.addConstr(d2[i][j][k] == abs_(d1[i][j][k]))
                    m.addConstr(c3[i][j][k] == or_(c1[i][j][k],c2[i][j][k]))
                    m.addConstr(c4[i][j][k] == and_(c3[i][j][k],c[i][k-1]))
                    m.addConstr((c4[i][j][k] == 1) >> (d2[i][j][k] >= 2))
                    m.addConstr((c4[i][j][k] == 0) >> (d2[i][j][k] >= 1))
        
        for i in range(veh_num):
            for j in range (veh_num):
                if i == j:
                    continue
                if allVeh[i].decision_num == allVeh[j].decision_num and allVeh[i].incLane == allVeh[j].incLane:
                    if allVeh[i].arrival_time > allVeh[j].arrival_time:
                        # print(i,j)
                        m.addConstr(d1[i][j][allVeh[i].decision_num] >= 1)
                for k in range(N):
                    m.addConstr((d3[i][j][k] == 1) >> (d1[i][j][k] >= 0.000001))
                    m.addConstr((d3[i][j][k] == 0) >> (d1[i][j][k] <= 0))
                    m.addConstr(d4[i][j][k] == and_(c1[i][j][k],d3[i][j][k]))
                    m.addConstr((d4[i][j][k] == 1) >> (d1[i][j][k] >= 1))
                    if k <= N - 3:
                        m.addConstr((d4[i][j][k] == 1) >> (d1[i][j][k + 1] >= 1))
                    elif k == N - 2:
                        m.addConstr((d4[i][j][k] == 1) >> (e[i] - e[j] >= 1))
        


        # for i in range (veh_num):
        #     for j in range(veh_num):
        #         m.addConstr((t1 == 1) >> (d_prime[i][N-1] ))


        a = Binary2("a",veh_num,veh_num)
        b =  Binary2("b",veh_num,veh_num)
        b_prime =  Binary2("b_p",veh_num,veh_num)
        W =  Cont2(0,12,"W",veh_num,veh_num)

        q =  Binary2("q",veh_num,veh_num)
        q_prime = Binary2("q_p",veh_num,veh_num)

        for i in range(veh_num):
            for j in range (veh_num):
                m.addConstr((a[i][j] == 1) >> (e[i] - e[j] >= 0.0001))
                m.addConstr((a[i][j] == 0) >> (e[i] - e[j] <= 0))
                if allVeh[i].leaveLane != allVeh[j].leaveLane:
                    m.addConstr(b[i][j] == 0)
                    m.addConstr(b_prime[i][j] == 1)
                else:
                    m.addConstr(b[i][j] == 1)
                    m.addConstr(b_prime[i][j] == 0)
                
                if allVeh[i].outLane != allVeh[j].outLane:
                    m.addConstr(q[i][j] == 0)
                    m.addConstr(q_prime[i][j] == 1)
                else:
                    m.addConstr(q[i][j] == 1)
                    m.addConstr(q_prime[i][j] == 0)
        
        a1 =  Binary3("a1",veh_num,veh_num)
        a2 =  Binary3("a2",veh_num,veh_num)
        a3 =  Binary3("a3",veh_num,veh_num)
        a4 =  Binary3("a4",veh_num,veh_num)
        a5 =  Binary2("a5",veh_num,veh_num)
        a6 =  Binary3("a6",veh_num,veh_num)
        a7 =  Binary3("a7",veh_num,veh_num)
        a8 =  Binary3("a8",veh_num,veh_num)
        a9 =  Binary3("a9",veh_num,veh_num)
        a10 =  Binary2("a10",veh_num,veh_num)
        a11 =  Binary2("a11",veh_num,veh_num)
        a12 =  Binary2("a12",veh_num,veh_num)
        a13 =  Binary2("a13",veh_num,veh_num)
        a14 =  Binary2("a14",veh_num,veh_num)
        a15 =  Binary2("a15",veh_num,veh_num)
        a16 = Cont2(-300,300,"a16",veh_num,veh_num)
        a17 = Cont2(0,300,"a17",veh_num,veh_num)
        a18 =  Binary2("a18",veh_num,veh_num)
        # a18 = Cont2("a18",veh_num)

        

        for i in range(veh_num):
            for j in range (veh_num):
                if i == j:
                    continue
                for k in range(veh_num):
                    m.addConstr(a1[i][j][k] == and_([a[i][j],a[k][j],a[i][k]]))
                    m.addConstr(a2[i][j][k] == and_([a[j][i],a[j][k],a[k][i]]))
                    m.addConstr(a3[i][j][k] == or_([a1[i][j][k],a2[i][j][k]]))
                    m.addConstr(a4[i][j][k] == and_([a3[i][j][k],q[i][k]]))
                    m.addConstr(a6[i][j][k] == and_([a3[i][j][k],b[i][k]]))   

                m.addConstr(a5[i][j] == or_(a4[i][j]))
                m.addConstr((a5[i][j] == 0) >> (a12[i][j] == 1))
                m.addConstr((a5[i][j] == 1) >> (a12[i][j] == 0))
                m.addConstr(a11[i][j] == and_([a12[i][j],q[i][j],a[i][j]]))

                m.addConstr(a10[i][j] == or_(a6[i][j]))
                m.addConstr((a10[i][j] == 0) >> (a13[i][j] == 1))
                m.addConstr((a10[i][j] == 1) >> (a13[i][j] == 0))
                m.addConstr(a14[i][j]  == and_(a13[i][j],b[i][j],q_prime[i][j],a[i][j]))

                m.addConstr((a11[i][j] == 1) >> (W[i][j] == allVeh[i].w_equal[allVeh[j].number]))
                m.addConstr((a14[i][j] == 1) >> (W[i][j] == allVeh[i].w_plus[allVeh[j].number]))
                m.addConstr(a15[i][j] == or_(a11[i][j],a14[i][j]))
                m.addConstr((a15[i][j] == 0) >> (W[i][j] == 0))
                m.addConstr(a16[i][j] == e[i] - e[j])
                m.addConstr(a17[i][j] == abs_(a16[i][j]))
                m.addConstr((a17[i][j] >= W[i][j]))
                m.addConstr((b[i][j] == 1) >> (a17[i][j] >= 1))
                m.addConstr((q[i][j] == 1) >> (a17[i][j] >= 1))
            
        # m.addConstr(a14[0][2] == 1)?

        for i in range(veh_num):
            m.addConstr(e1[i] == e[i] - allVeh[i].arrival_time - 15)

        m.addConstr(maxtime == max_(e),name="maxconstr")
        m.setObjective(maxtime, GRB.MINIMIZE)
                    
                    
                    
                
                
        



        

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
            if 'a' in v.varName or 'e_' in v.varName or 'd_' in v.varName  or 'W_' in v.varName or 'q_' in v.varName:
                print('%s %g' % (v.varName, v.x))
        
        for i in range(len(allVeh)):
            print(allVeh[i].ID)
        


        print('Obj: %g' % m.objVal)

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

# A = [Vehicle("A_1",1,0,0,1,1),Vehicle("A_2",2,0,0,0,3)]
# B = [Vehicle("B_1",1,1,1,1,2),Vehicle("B_2",3,1,1,1,4)]
# C = [Vehicle("C_1",1,2,2,2,11),Vehicle("C_2",3,2,2,2,12)]

# A = [Vehicle("A_1",1,0,0,1,1),Vehicle("A_2",2,0,0,0,3),Vehicle("A_3",3,0,0,1,5),Vehicle("A_4",4,0,0,0,7),Vehicle("A_5",16,0,1,2,9)]
# B = [Vehicle("B_1",1,1,1,1,2),Vehicle("B_2",3,1,1,1,4),Vehicle("B_3",4,1,1,1,6),Vehicle("B_4",5,1,1,1,8),Vehicle("B_5",15,1,1,2,10)]
# C = [Vehicle("C_1",1,2,2,2,11),Vehicle("C_2",3,2,2,2,12),Vehicle("C_3",4,2,2,2,13),Vehicle("C_4",5,2,2,2,14),Vehicle("C_5",15,2,1,2,15)]
# allVeh = deal_input(4,sys.argv[1])
# # allVeh = A + B + C
# allVeh.sort(key=myFunc)
# allVeh = W_init(allVeh)
# print(allVeh[4].w_equal)
# veh_num = len(allVeh)
m = Model("mip1")
# milp(m,3,3)
