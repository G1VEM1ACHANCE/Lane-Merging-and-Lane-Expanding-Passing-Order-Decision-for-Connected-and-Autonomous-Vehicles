from gurobipy import *
import sys
import numpy as np
import random
class Vehicle:
    def __init__(self,ID,arrival_time,lane,number):
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
# B = [Vehicle("B_1",1,'B',2),Vehicle("B_2",3,'B',4),Vehicle("B_3",4,'B',6),Vehicle("B_4",5,'B',8),Vehicle("B_5",8,'B',10)]

A = [Vehicle("A_1",1,'A',1),Vehicle("A_2",2,'A',3),Vehicle("A_3",3,'A',5),Vehicle("A_4",4,'A',7)]
B = [Vehicle("B_1",1,'B',2),Vehicle("B_2",3,'B',4),Vehicle("B_3",4,'B',6),Vehicle("B_4",5,'B',8)]

W_init(A,B)
print("aaaa")
print(A[0].w_equal)
allVeh = A.copy() + B.copy()
allVeh.sort(key=myFunc)
veh_num = len(allVeh)

try:
    # Create a new model
    m = Model("mip1")
    m.setParam('Method', 0)
    decision_num = 1
    # Create variables
    N = 10
    T = 2
    M = 300
    e = Cont1("e",veh_num)
    d_prime = Cont1("d_p",veh_num)
    d = Cont1("d",veh_num)
    l = Int1(0,1,"l",veh_num)
    o = Int1(0,2,"o",veh_num)
    #arrival time ind
    a = Binary2("a",veh_num)
    a_prime =  Binary2("a_p",veh_num)
    a1 =  Binary3("a1",veh_num)
    a2 =  Binary3("a2",veh_num)
    a3 =  Binary3("a3",veh_num)
    a4 =  Binary3("a4",veh_num)
    a5 =  Binary2("a5",veh_num)
    a6 =  Binary3("a6",veh_num)
    a7 =  Binary3("a7",veh_num)
    a8 =  Binary3("a8",veh_num)
    a9 =  Binary3("a9",veh_num)
    a10 =  Binary2("a10",veh_num)
    a11 =  Binary2("a11",veh_num)
    a12 =  Binary2("a12",veh_num)
    a13 =  Binary2("a13",veh_num)
    a14 =  Binary2("a14",veh_num)
    a15 =  Binary2("a15",veh_num)
    a16 = Cont2("a16",veh_num)
    a17 = Cont2("a17",veh_num)
    a18 = Cont2("a18",veh_num)
    #same income ind
    b =  Binary2("b",veh_num)
    b_prime =  Binary2("b_p",veh_num)
    b1 =  Int2("b1",veh_num)
    b2 =  Int2("b2",veh_num)
    b3 =  Int2("b3",veh_num)
    #same outgo ind
    c =  Binary2("c",veh_num)
    c_prime = Binary2("c_p",veh_num)
    c1 =  Int2("c1",veh_num)
    c2 =  Int2("c2",veh_num)
    c3 =  Int2("c3",veh_num)


    p =  Binary1("p",veh_num)
    p1 =  Int1(-1,1,"p1",veh_num)
    p2 =  Int1(0,1,"p2",veh_num)
    p3 =  Binary2("p3",veh_num)
    p4 =  Int2("p4",veh_num)
    p5 =  Int2("p5",veh_num)
    p6 =  Binary2("p6",veh_num)
    p7 =  Binary2("p7",veh_num)
    p8 =  Binary2("p8",veh_num)
    p9 =  Binary2("p9",veh_num)
    f = Cont2("f",veh_num)
    f1 = Cont2("f1",veh_num)
    f2 = Cont2("f2",veh_num)

    q = Int1(-1,1,"q",veh_num)
    q1 = Int1(0,1,"q1",veh_num)


    W =  Cont2("W",veh_num)

    s = Int1(0,1,"s",veh_num)

    t = Binary2("t",veh_num)
    t1 = Binary2("t1",veh_num)

    maxtime = m.addVar(vtype=GRB.CONTINUOUS, name="maxtime")
    
  
    
    # Integrate new variables
    m.update()
    # for v in m.getVars():
    #    print('%s %g' % (v.varName, v.x))
     # Set objective
    # # Add constraint: x + 2 y + 3 z <= 4
    for i in range(veh_num):
        m.addConstr(e[i] >= d_prime[i] + 20, "earliest_enter")
        m.addConstr(d_prime[i] >= d[i],"decision_constr1")
        m.addConstr(d[i] >= allVeh[i].arrival_time + 30,"decision_constr2")
        #m.addConstr(o[i] >= l[i],"lane_constr")


    for i in range(veh_num):
        for j in range (veh_num):
            m.addConstr((a[i][j] == 1) >> (e[i] - e[j] >= 0.0001))
            m.addConstr((a[i][j] == 0) >> (e[i] - e[j] <= 0))
            m.addConstr((b1[i][j] == o[i] - o[j]))
            m.addConstr(b2[i][j] == abs_(b1[i][j]))
            m.addConstr((b[i][j] == 1) >> (b2[i][j] == 0)) #oi = oj b = 1
            m.addConstr((b[i][j] == 0) >> (b2[i][j] - 1 >= 0)) #oi != oj bprime = 1
            m.addConstr((b_prime[i][j] == 0) >> (b2[i][j] == 0))
            m.addConstr((b_prime[i][j] == 1) >> (b2[i][j] - 1 >= 0))
            m.addConstr((c1[i][j] == l[i] - l[j]))
            m.addConstr(c2[i][j] == abs_(c1[i][j]))
            m.addConstr((c[i][j] == 1) >> (c2[i][j] == 0)) #li = lj c = 1
            m.addConstr((c[i][j] == 0) >> (c2[i][j] - 1 >= 0)) 
            m.addConstr((c_prime[i][j] == 0) >> (c2[i][j] == 0))
            m.addConstr((c_prime[i][j] == 1) >> (c2[i][j] - 1 >= 0))#li != lj cprime = 1
    
    for i in range (veh_num):
        for j in range(veh_num):
            if allVeh[i].arrival_time > allVeh[j].arrival_time and allVeh[i].lane == allVeh[j].lane:
                m.addConstr(d[i] - d[j] >= 0.000001)
                m.addConstr(t[i][j] == 1)
            else:
                m.addConstr(t[i][j] == 0)
            m.addConstr((t[i][j] == 1) >> (d_prime[i] - d_prime[j] >= 1))
            m.addConstr((t[i][j] == 1) >> (e[i] - e[j] >= 1))
            #m.addConstr((t1[i][j] == 1) >> (e[i] - e[j] >= allVeh[i].w_equal[j]))
    for i in range(veh_num):
        for j in range (veh_num):
            if i == j:
                continue
            for k in range(veh_num):
                m.addConstr(a1[i][j][k] == and_([a[i][j],a[k][j],a[i][k]]))
                m.addConstr(a2[i][j][k] == and_([a[j][i],a[j][k],a[k][i]]))
                m.addConstr(a3[i][j][k] == or_([a1[i][j][k],a2[i][j][k]]))
                m.addConstr(a4[i][j][k] == and_([a3[i][j][k],b[i][k]]))   
                m.addConstr((a3[i][j][k] == 0) >> (a6[i][j][k] == 1)) #a6 = 1 no cars between i,j
                # m.addConstr(a7[i][j][k] == and_(a6[i][j][k])
                m.addConstr(a8[i][j][k] == and_([a3[i][j][k],b_prime[k][j]]))
                m.addConstr(a9[i][j][k] == or_([a6[i][j][k], a8[i][j][k]]))

            m.addConstr(a5[i][j] == or_(a4[i][j]))
            m.addConstr(a11[i][j] == and_([a5[i][j],b[i][j]]))
            m.addConstr(a12[i][j] == or_([a11[i][j],b_prime[i][j]]))
            m.addConstr(a10[i][j] == and_(a9[i][j]))
            m.addConstr(a13[i][j] == and_([a10[i][j],b[i][j]]))
            m.addConstr((a12[i][j] == 1) >> (W[i][j] == 0))
            m.addConstr(a14[i][j] == and_([c[i][j],a13[i][j]]))
            m.addConstr(a15[i][j] == and_([c_prime[i][j],a13[i][j]]))
            m.addConstr((a14[i][j] == 1) >> (W[i][j] == allVeh[i].w_equal[j]))
            m.addConstr((a15[i][j] == 1) >> (W[i][j] == allVeh[i].w_plus[j]))
            m.addConstr(a16[i][j] == e[i] - e[j])
            m.addConstr(a17[i][j] == abs_(a16[i][j]))
            m.addConstr((a17[i][j] >= W[i][j]))

            # m.addConstr((a[i][j] == 0) >> (e[i] - e[j] >= W[i][j]))
    
    for i in range(veh_num):
        if allVeh[i].incLane == 0:
            m.addConstr(s[i] == 0)
        else:
            m.addConstr(s[i] == 1)
        m.addConstr(p1[i] == l[i] - s[i])
        m.addConstr(p2[i] == abs_(p1[i]))
        m.addConstr((p[i] == 0) >> (p2[i] == 0)) #pi = 0 if si = li
        m.addConstr((p[i] == 1) >> (p2[i] - 1 >= 0))
        # m.addConstr(p[1] == 1)
        # m.addConstr(p[3] == 1)
        
    for i in range (veh_num):
        m.addConstr(q[i] == o[i] - l[i])
        m.addConstr(q[i] <= 1)
        m.addConstr(q[i] >= 0)


    for i in range(veh_num):
        for j in range(veh_num):
            if i == j:
                continue
            m.addConstr(p4[i][j] == l[i] - s[j])
            m.addConstr(p5[i][j] == abs_(p4[i][j]))
            m.addConstr((p3[i][j] == 1) >> (p5[i][j] == 0)) #p3 = 1 if li = sj
            m.addConstr((p3[i][j] == 0) >> (p5[i][j] - 1 >= 0))
            m.addConstr(p6[i][j] == or_([p3[i][j],c[i][j]]))
            m.addConstr(p7[i][j] == and_([p6[i][j],p[i]]))
            m.addConstr(f1[i][j] == d_prime[i] - d_prime[j])
            m.addConstr(f2[i][j] == abs_(f1[i][j]))
            m.addConstr((p7[i][j] == 1) >> (f2[i][j] >= T))
            if allVeh[i].incLane == allVeh[j].incLane:
                m.addConstr(f2[i][j] >= 1)
            
    u = Binary1("u",veh_num)
    v = Binary1("v",veh_num)
    w = Binary1("w",veh_num)

    v2 = Int1(-1,1,"v2",veh_num)
    v3 = Int1(0,1,"v3",veh_num)

    u1 = m.addVar(lb = 0,ub = 60,vtype=GRB.INTEGER)
    v1 = m.addVar(lb = 0,ub = 60,vtype=GRB.INTEGER)
    w1 = m.addVar(lb = 0,ub = 60,vtype=GRB.INTEGER)

    for i in range (veh_num):
        m.addConstr((u[i] == 1) >> (o[i] == 0))
        m.addConstr((u[i] == 0) >> (o[i] >= 1))
        m.addConstr((v2[i] == o[i] - 1))
        m.addConstr((v3[i] == abs_(v2[i])))
        m.addConstr((v[i] == 1) >> (v3[i] == 0))
        m.addConstr((v[i] == 0) >> (v3[i] == 1))
        m.addConstr((w[i] == 0) >> (o[i] <= 1))
        m.addConstr((w[i] == 1) >> (o[i] == 2))

    m.addConstr(u1 == quicksum(u[i] for i in range (veh_num)))
    m.addConstr(v1 == quicksum(v[i] for i in range (veh_num)))
    m.addConstr(w1 == quicksum(w[i] for i in range (veh_num)))
    # m.addConstr(o[0] == 0)
    # m.addConstr(o[1] == 0)
    # m.addConstr(o[2] == 1)
    # m.addConstr(o[3] == 1)
    # m.addConstr(o[4] == 2)
    # m.addConstr(o[5] == 2)
    

        

    m.setObjective((u1*u1 + v1*v1 + w1*w1) /3 - (u1+v1+w1)*(u1+v1+w1)/9, GRB.MINIMIZE)       
    
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
