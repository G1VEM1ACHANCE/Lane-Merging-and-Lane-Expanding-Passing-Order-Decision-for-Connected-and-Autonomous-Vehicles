from gurobipy import *
import sys
import numpy as np
import random


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
    return e.arrival_time


def Binary1(m,name,veh_num):
    temp = []
    for i in range(veh_num):
        temp.append(m.addVar(vtype=GRB.BINARY,name= name + '_' +  str(i)))
    return temp

def Int1(m,lb,ub,name,veh_num):
    temp = []
    for i in range(veh_num):
        temp.append(m.addVar(lb = lb, ub = ub,vtype=GRB.INTEGER,name= name + "_" + str(i)))
    return temp


def Cont1(m,name,veh_num):
    temp = []
    for i in range(veh_num):
        temp.append(m.addVar(lb = 0, ub = 300, vtype=GRB.CONTINUOUS,name= name + "_" + str(i)))
    return temp

def Binary2(m,name,num1,num2):
    temp = []
    for i in range(num1):
        temp1 = []
        for j in range (num2):
            temp1.append(m.addVar(vtype=GRB.BINARY,name=name + "_" + str(i) + "_"  + str(j)))
        temp.append(temp1)
    return temp

def Int2(m,lb,ub,name,a,b):
    temp = []
    for i in range(a):
        temp1 = []
        for j in range (b):
            temp1.append(m.addVar(lb = lb, ub = ub,vtype=GRB.INTEGER,name=name + "_"  + str(i)+ "_"  + str(j)))
        temp.append(temp1)
    return temp

def Cont2(m,name,veh_num):
    temp = []
    for i in range(veh_num):
        temp1 = []
        for j in range (veh_num):
            temp1.append(m.addVar(lb = -300, ub = 300,vtype=GRB.CONTINUOUS,name= name + "_"  + str(i) + "_"  + str(j)))
        temp.append(temp1)
    return temp

def Binary3(m,name,veh_num,N,M):
    temp = []
    for i in range(veh_num):
        temp1 = []
        for j in range (N):
            temp2 = []
            for k in range(M):
                temp2.append(m.addVar(vtype=GRB.BINARY,name= name + "_" + str(i) + "_" + str(j) + "_" + str(k)))
            temp1.append(temp2)
        temp.append(temp1)
    return temp

def Cont3(m,name,veh_num):
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

def deal_change(M,N):
    arr = np.zeros((M,N,M))
    if M == N-1:
        for k in range(M):
            for i in range(M):
                for j in range(N):
                    # print(i,j,k)
                    if k == 0 and j - i <= 1 and j - i >= 0:
                        # print(i,j,k)
                        arr[i][j][k] = 1
                    if k > 0:
                        for s in range(M):
                            # if i == 0 and j == 2 and s == 1 and k == 1:
                             # print(abs(i - s),arr[s][j][k - 1])
                            if abs(i - s) <= k and arr[s][j][0] == 1:
                                arr[i][j][k] = 1
    if M == N - 2:
        for k in range(M):
            for i in range(M):
                for j in range(N):
                    # print(i,j,k)
                    if k == 0:
                        if i == M - 1:
                            arr[i][N-1][k] = 1
                            arr[i][N-2][k] = 1
                        elif j - i <= 1 and j - i >= 0:
                        # print(i,j,k)
                            arr[i][j][k] = 1
                    if k > 0:
                        for s in range(M):
                            # if i == 0 and j == 2 and s == 1 and k == 1:
                                # print(abs(i - s),arr[s][j][k - 1])
                            if abs(i - s) <= k and arr[s][j][0] == 1:
                                arr[i][j][k] = 1
    if M == N - 3:
        for k in range(M):
            for i in range(M):
                for j in range(N):
                    # print(i,j,k)
                    if k == 0:
                        if i == M - 1:
                            arr[i][N-1][k] = 1
                            arr[i][N-2][k] = 1
                        elif i == M - 2:
                            arr[i][N-4][k] = 1
                            arr[i][N-3][k] = 1
                        elif j - i <= 1 and j - i >= 0:
                        # print(i,j,k)
                            arr[i][j][k] = 1
                    if k > 0:
                        for s in range(M):
                            # if i == 0 and j == 2 and s == 1 and k == 1:
                                # print(abs(i - s),arr[s][j][k - 1])
                            if abs(i - s) <= k and arr[s][j][0] == 1:
                                arr[i][j][k] = 1
    print(arr)
    return arr
                    




def printKey(A,B):
    for i in range (len(A)):
        print(A[i].lane,A[i].k)
    for i in range (len(B)):
        print(B[i].lane,B[i].k)

def deal_input(N,infile):
    f = open(infile,"r")
    arr = []
    for i in range(N):
        arr.append([])
    temp_in = f.readline()
    while (len(temp_in) > 0):
        x = temp_in.split(" ")
        arr[ord(x[2]) - ord('A')].append(Vehicle(x[0],eval(x[1]),x[2],eval(x[3])))
        temp_in = f.readline()
    # for i in range(len(A)):
    #     print(A[i].ID,A[i].arrival_time,A[i].lane,A[i].number,A[i].w_equal,A[i].w_plus)
    return arr

# A = [Vehicle("A_1",1,'A',1),Vehicle("A_2",2,'A',3),Vehicle("A_3",3,'A',5),Vehicle("A_4",4,'A',7),Vehicle("A_5",40,'A',9)]
# B = [Vehicle("B_1",1,'B',2),Vehicle("B_2",3,'B',4),Vehicle("B_3",4,'B',6),Vehicle("B_4",5,'B',8),Vehicle("B_5",20,'B',10)]

# A = [Vehicle("A_1",1,'A',1),Vehicle("A_2",2,'A',3),Vehicle("A_3",3,'A',5),Vehicle("A_4",4,'A',7)]
# B = [Vehicle("B_1",1,'B',2),Vehicle("B_2",3,'B',4),Vehicle("B_3",4,'B',6),Vehicle("B_4",5,'B',8)]
def model_solution(m,allVeh):
    leave = []
    out = []
    for v in m.getVars():
            # if 'd_' in v.varName or 'e_' in v.varName or 'l_' in v.varName or 'o_' in v.varName or 'W_' in v.varName or 'p_' in v.varName:
            # if 'l_' in v.varName or 'c_' in v.varName:
        if 'l_' in v.varName:
            leave.append(v.x)
        elif 'o_' in v.varName:
            out.append(v.x)
        elif 'u1' in v.varName:
            print(v.varName,v.x)

    for i in range (len(allVeh)):
        allVeh[i].outLane = round(leave[i])
        allVeh[i].leaveLane = round(out[i])
    
    allVeh.sort(key=myFunc)

    return allVeh 
    






def milp1(m,M,N,allVeh):

    # m.setParam('TimeLimit', 60)
    veh_num = len(allVeh)

    P = 15
    CanChange = deal_change(M,N)

    eachlane = []
    for i in range (N):
        eachlane.append(veh_num // N)
    for j in range(veh_num % N):
        eachlane[j] += 1
    try:
        # Create a new model
        decision_num = 1
        # Create variables

        # Integrate new variables
        m.update()

        o = Int1(m,0,N-1,"o",veh_num)
        o1 = Binary2(m,"o1",veh_num,N)
        a1 = Int2(m,- N - 1,N-1,"a1",veh_num,N)
        a2 = Int2(m,0,N-1,"a2",veh_num,N)
        c = Int1(m,0,M-1,"c",veh_num)
        l = Int1(m,0,M-1,"l",veh_num)
        l1 = Binary2(m,"l1",veh_num,M)
        c1 = Int1(m,-N - 1,N-1,"c1",veh_num)
        a3 = Int2(m,- M - 1,M-1,"a3",veh_num,M)
        a4 = Int2(m,0,M-1,"a4",veh_num,M)
        b = Binary3(m,"b",veh_num,M,N)


        for i in range(veh_num):
            temp = allVeh[i].arrival_time // P
            if temp >= M - 1:
                temp = M - 1
            allVeh[i].k = int(temp)
            # print(allVeh[i].ID,temp)
        
        for i in range(veh_num):
            m.addConstr(o[i] >= 0)
            m.addConstr(o[i] <= N - 1)
            # m.addConstr(l[i] - allVeh[i].incLane <= allVeh[i].k)
            
            for j in range(N):
                # print(allVeh[i].lane,j,allVeh[i].k)
                m.addConstr(a1[i][j] == o[i] - j)
                m.addConstr(a2[i][j] == abs_(a1[i][j]))
                m.addConstr((o1[i][j] == 1) >> (a2[i][j] == 0))
                m.addConstr((o1[i][j] == 0) >> (a2[i][j] >= 1))
                if CanChange[allVeh[i].incLane][j][allVeh[i].k] == 0:
                    m.addConstr(a2[i][j] >= 1)

            for j in range(M):
                m.addConstr(a3[i][j] == l[i] - j)
                m.addConstr(a4[i][j] == abs_(a3[i][j]))
                m.addConstr((l1[i][j] == 1) >> (a4[i][j] == 0))
                m.addConstr((l1[i][j] == 0) >> (a4[i][j] >= 1))
            
            for j in range(M):
                for k in range (N):
                    m.addConstr(b[i][j][k] == and_(l1[i][j],o1[i][k]))
                    if CanChange[j][k][0] == 0:
                        m.addConstr(b[i][j][k] == 0)



                
                    
                    
            



        lane_veh = []

        for j in range (N):
            u = Binary1(m,"u_" + str(j),veh_num)
            v2 = Int1(m,-N,N,"v2_" + str(j),veh_num)
            v3 = Int1(m,0,N,"v3_"+ str(j),veh_num)
            for i in range (veh_num):
                m.addConstr((v2[i] == o[i] - j))
                m.addConstr((v3[i] == abs_(v2[i])))
                m.addConstr((u[i] == 1) >> (v3[i] == 0))
                m.addConstr((u[i] == 0) >> (v3[i] >= 1))
            u1 = m.addVar(lb = 0,ub = 60,vtype=GRB.INTEGER,name="u1" + '_' + str(j))
            lane_veh.append(u1)
            m.addConstr(u1 == quicksum(u[i] for i in range (veh_num)))
        
        changes = m.addVar(vtype=GRB.INTEGER,name="changes")
        for i in range(veh_num):
            m.addConstr(c1[i] == l[i] - allVeh[i].incLane)
            m.addConstr(c[i] == abs_(c1[i]))
            m.addConstr(c[i] <= allVeh[i].k)
        m.addConstr(changes == quicksum(c[i] for i in range(veh_num)))


        # m.addConstr(o[0] == 0)
        # m.addConstr(o[1] == 0)
        # m.addConstr(o[2] == 1)
        # m.addConstr(o[3] == 1)
        # m.addConstr(o[4] == 3)
        # m.addConstr(o[5] == 2)
        fanjun = 0
        junfan = 0
        for i in range (N):
            fanjun += lane_veh[i] * lane_veh[i]
            junfan += lane_veh[i]
        fanjun /= N
        junfan = junfan *junfan / N / N
        kk = m.addVar(name="kk")
        ll = m.addVar(name="ll")
        m.addQConstr(kk == fanjun)
        m.addQConstr(ll == junfan)
        m.addQConstr(kk - ll >= np.var(eachlane))

        
        



            
        # m.setObjective(u, GRB.MINIMIZE)   
        m.setObjective(kk - ll, GRB.MINIMIZE)       
        
        m.optimize()
        m.write('mip1.lp')
        if m.status == GRB.INFEASIBLE:
            # Compute the infeasible constraints and print them
            m.computeIIS()
            print("The following constraints are infeasible:")
            for c in m.getConstrs():
                if c.IISConstr:
                    print(c.constrName)


        print('Obj: %g' % m.objVal)

           


    
        # for i in range(len(allVeh)):
        #     print(allVeh[i].ID,allVeh[i].lane,l[i].x,o[i].x,c[i].x)

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
    return allVeh

# m = Model("mip1")
# milp1(m,4,5)