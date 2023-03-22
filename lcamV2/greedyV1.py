import numpy as np 
from test import Vehicle

# class Vehicle:
#     def __init__(self,ID,arrival_time,lane,number,w_equal,w_plus):

#         self.ID = ID 
#         self.arrival_time = arrival_time
#         self.position = -1
#         self.speed = 1
#         self.incLane = lane
#         self.lane = lane
#         self.number = number
#         self.decision_arrive = -1
#         self.decision_depart = -1
#         self.ifChange = 0
#         self.passingOrder = -1
#         self.w_equal = w_equal
#         self.w_plus = w_plus
#         self.waiting = 0

def myFunc(e):
    return e.arrival_time
    
def print_order(A,B):
    for i in range (len(A)):
        print(A[i].ID,A[i].passingOrder,A[i].ifChange,A[i].decision_depart)
    for i in range (len(B)):
        print(B[i].ID,B[i].passingOrder,B[i].ifChange,B[i].decision_depart)


D_safe = 4


def FCFS(A,B):
    D_safe = 4
    tempA = A.copy()
    tempB = B.copy()
    temp = tempA + tempB
    temp.sort(key=myFunc)

    for i in range(len(temp)):
        if temp[i] in A:
            A[A.index(temp[i])].passingOrder = i
        if temp[i] in B:
            B[B.index(temp[i])].passingOrder = i
        temp[0].decision_depart = 0
    for i in range(1,len(temp)):
        idx = -1
        if temp[i] in A:
            idx = A.index(temp[i])
        else:
            idx = B.index(temp[i])
        time = []
        if temp[i].incLane != temp[i-1].incLane:
            time = [max(temp[i].arrival_time,temp[i-1].decision_depart + max(temp[i-1].w_equal[temp[i].number],D_safe)),max(temp[i].arrival_time,temp[i-1].decision_depart +temp[i-1].w_plus[temp[i].number])]
        else:
            time = [max(temp[i].arrival_time,temp[i-1].decision_depart + temp[i-1].w_equal[temp[i].number]),max(temp[i].arrival_time,temp[i-1].decision_depart + max(temp[i-1].w_plus[temp[i].number],D_safe))]
        temp[i].decision_depart = min(time)
        minidx = time.index(min(time))
        if min(time) == temp[i].arrival_time:
            temp[i].ifChange = 0
        elif minidx == 0:
            if temp[i].incLane != temp[i-1].lane:
                temp[i].ifChange = 1
        elif minidx == 1:
            if temp[i].incLane == temp[i-1].lane:
                temp[i].ifChange = 1
        if temp[i].ifChange == 1:
            if temp[i].incLane == 'A':
                temp[i].lane = 'B'
                A[idx] = temp[i]
            else:
                temp[i].lane = 'A'
                B[idx] = temp[i]
        else:
            if temp[i].incLane == 'A':
                temp[i].lane = 'A'
                A[idx] = temp[i]
            else:
                temp[i].lane = 'B'
                B[idx] = temp[i]
    #print_order(A,B)
    for i in range (len(A)):
        A[i].decision_depart = -1
    for i in range(len(B)):
        B[i].decision_depart = -1
    return A,B

            

            

    



if __name__ == "__main__":
    A = [Vehicle("A_1",3,'A',0,[0,2,7,3,3],[0,3,7,4,4]),Vehicle("A_2",6,'A',2,[7,2,0,2,3],[7,7,0,7,4]),Vehicle("A_3",9,'A',4,[3,3,3,3,0],[4,4,4,4,0])]
    B = [Vehicle("B_1",4,'B',1,[2,0,2,4,3],[3,0,7,5,4]),Vehicle("B_2",7,'B',3,[3,4,2,0,3],[4,5,7,0,4])]
    Ａ,B = FCFS(A,B)
    print_order(A,B)