import numpy as np 
import random,copy


time = 0
decision_point = 20
lane_len = 50
Tc = 2
output = []
tempout = []
passing_count = 0
isOccupied = -1 
result = []


def W_init(A,B):
    for i in range (len(A)):
        for j in range (len(A)):
            if i == j:
                continue
            num = random.randint(1,5)
            A[i].w_equal.append((A[j].ID,num))
            A[i].w_plus.append((A[j].ID,num + 2))
        for j in range (len(B)):
            num = random.randint(1,5)
            A[i].w_equal.append((B[j].ID,num))
            A[i].w_plus.append((B[j].ID,num + 2))
    for i in range (len(B)):
        for j in range (len(A)):
            num = random.randint(1,5)
            B[i].w_equal.append((A[j].ID,num))
            B[i].w_plus.append((A[j].ID,num + 2))
        for j in range (len(B)):
            if i == j:
                continue
            num = random.randint(1,5)
            B[i].w_equal.append((B[j].ID,num))
            B[i].w_plus.append((B[j].ID,num + 2))


            

def myFunc(e):
    return e.arrival_time

def FCFS(A,B):
    tempA = A.copy()
    tempB = B.copy()
    temp = tempA + tempB
    temp.sort(key=myFunc)

    for i in range(len(temp)):
        if temp[i] in A:
            A[A.index(temp[i])].passingOrder = i
        if temp[i] in B:
            B[B.index(temp[i])].passingOrder = i
    # for i in range(len(A)):
    #     A[i].ifChange = 0#random.randint(0,1)
    # for i in range(len(B)):
    #     B[i].ifChange = (i + 1) % 2#random.randint(0,1)
    return A,B
    
    
    


class Vehicle:
    def __init__(self,ID,arrival_time,lane,number,w_equal,w_plus):
        self.ID = ID 
        self.arrival_time = arrival_time
        self.position = -1
        self.speed = 1
        self.incLane = lane
        self.lane = lane
        self.number = number
        self.decision_arrive = -1
        self.decision_depart = -1
        self.scheduled_enter = -1
        self.ifChange = 0
        self.passingOrder = -1
        self.w_equal = w_equal
        self.w_plus = w_plus
        self.waiting = 0

def printPos(A):
    for i in range(len(A)):
        print(A[i].ID,A[i].position,A[i].lane,A[i].ifChange,A[i].position)
    print("\n")


def pos_init(L,t):
    for i in range(len(L)):
        if L[i].arrival_time == t:
            L[i].position = lane_len

def check_pre_decision_point(L,t,temp):
    for i in range (len(L)):
        L[i].speed = 1
        if L[i].position == decision_point + Tc:
            idx = temp.index(L[i])
            for j in range (idx):
                if (temp[j].ifChange != 0 or temp[idx].ifChange != 0) and temp[j].position >= decision_point:
                    L[i].speed = 0
                    temp[idx].speed = 0
    
                
            

def check_decision_point(L,t,temp):
    for i in range(len(L)):
        if L[i].decision_arrive == -1 and L[i].position == decision_point:
            L[i].decision_arrive = t
        if L[i].decision_arrive != -1 and L[i].position != decision_point and L[i].decision_depart == -1:
            L[i].decision_depart = t
            temp.pop(0)
            
            



def lane_change_check_A(A,B):
    for veh in range(len(A)):
        if A[veh].position == decision_point:
            if A[veh].ifChange == 1:
                for i in range(len(B)):
                    if abs(B[i].position - A[veh].position) < Tc:
                        A[veh].speed = 0
                        return
                for i in range (veh):
                    if A[veh].position - A[i].position < Tc and A[veh].lane != A[i].lane:
                        A[veh].speed = 0
                        return 
                A[veh].lane = "B"


def lane_change_check_B(A,B):
    for veh in range (len(B)):
        if B[veh].position == decision_point:
            if B[veh].ifChange == 1:
                for i in range(len(A)):
                    if abs(A[i].position - B[veh].position) < Tc:
                        B[veh].speed = 0
                        return 
                for i in range (veh):
                    if B[veh].position - B[i].position < Tc and B[veh].lane != B[i].lane:
                        B[veh].speed = 0
                        return
                B[veh].lane = "A"
    
def dist_check(L):
    for i in range(len(L)):
        for j in range (i):
            if L[i].position - L[j].position == 1 and L[j].speed == 0:
                L[i].speed = 0


def move(A,B,t,last_vehicle):
    for i in range (len(A)):
        A[i].position -= A[i].speed
    if len(A) > 0 and A[0].position < 0 and t > 20:
        behavior = {}
        behavior['arrival_time'] = A[0].arrival_time
        behavior['decision_arrive'] = A[0].decision_arrive
        behavior['decision_depart'] = A[0].decision_depart
        behavior['lane'] = A[0].lane
        behavior['ID'] = A[0].ID
        A[0].scheduled_enter = t
        behavior['scheduled_enter'] = A[0].scheduled_enter
        behavior['waiting'] = A[0].waiting
        print(A[0].waiting,A[0].ID,A[0].scheduled_enter)
        last_vehicle = copy.deepcopy(A[0])
        output.append(behavior)
        A.pop(0)

    for j in range (len(B)):
        B[j].position -= B[j].speed
    if len(B) > 0 and B[0].position < 0 and t > 20:
        behavior = {}
        behavior['arrival_time'] = B[0].arrival_time
        behavior['decision_arrive'] = B[0].decision_arrive
        behavior['decision_depart'] = B[0].decision_depart
        behavior['lane'] = B[0].lane
        behavior['ID'] = B[0].ID
        behavior['waiting'] = B[0].waiting
        B[0].scheduled_enter = t
        behavior['scheduled_enter'] = B[0].scheduled_enter
        last_vehicle = copy.deepcopy(B[0])
        print(B[0].waiting,B[0].ID,B[0].scheduled_enter)
        output.append(behavior)
        B.pop(0)
    return last_vehicle

def pass_check(L,t,last_vehicle):
    for i in range (len(L)):
        if L[i].passingOrder == 0:
            continue
        if L[i].position == 0:
            if last_vehicle != None and L[i].passingOrder == last_vehicle.passingOrder + 1:
                waiting = 0
                if L[i].lane == last_vehicle.lane:
                    waiting = L[i].w_equal[last_vehicle.number]
                if L[i].lane != last_vehicle.lane:
                    waiting = L[i].w_plus[last_vehicle.number]
                L[i].waiting = waiting
                if t - last_vehicle.scheduled_enter < waiting:
                    L[i].speed = 0
            else:
                L[i].speed = 0



                
                
                



        

def lane_change_merge(A,B):
    temp = A.copy() + B.copy()
    temp.sort(key=myFunc)
    last_vehicle = None
    for i in range(200):
        pos_init(A,i)
        pos_init(B,i)
        # if (B[1].position == 22):
        #     printPos(A)
        #     printPos(B)
        #printPos(temp)

        check_pre_decision_point(A,i,temp)
        check_pre_decision_point(B,i,temp)
        
        

        lane_change_check_A(A,B)
        lane_change_check_B(A,B)

        check_decision_point(A,i,temp)
        check_decision_point(B,i,temp)

        dist_check(A)
        dist_check(B)

        pass_check(A,i,last_vehicle)
        pass_check(B,i,last_vehicle)
        
        last_vehicle = move(A,B,i,last_vehicle)
        

        if len(A) == 0 and len(B) == 0 and i > 20:
            return
            
    


    


        

#'''

if __name__ == "__main__":
    # A = [Vehicle("A_1",1,'A'),Vehicle("A_2",2,'A'),Vehicle("A_3",3,'A'),Vehicle("A_4",4,'A'),Vehicle("A_5",16,'A')]
    # B = [Vehicle("B_1",1,'B'),Vehicle("B_2",3,'B'),Vehicle("B_3",4,'B'),Vehicle("B_4",5,'B'),Vehicle("B_5",8,'B')]
    deal_input()
    # FCFS(A,B)
    # W_init(A,B)
    # lane_change_merge(A,B)
    # print(output)
#