import numpy as np 
from test import Vehicle
import test

def nldp(A,B):
    D_safe = 4
    L_A = np.zeros([len(A) + 1,len(B) + 1])
    L_B = np.zeros([len(A) + 1,len(B) + 1])
    L_A[0][0] = 0
    L_B[0][0] = 0
    L_A[1][0] = A[0].arrival_time
    L_B[0][1] = A[1].arrival_time

    steps = np.zeros([2,len(A) + 1,len(B) + 1])
    

    for i in range(2,len(A) + 1):
        L_A[i][0] = max(A[i-1].arrival_time,L_A[i-1][0] + A[i-1].w_equal[A[i-2].number])
        steps[0][i][0] = 0
    for j in range(2,len(B) + 1):
        L_B[0][j] = max(B[j-1].arrival_time,L_B[0][j-1] + B[j-1].w_equal[B[j-2].number])
        steps[1][0][j] = 1
    
    for i in range (1,len(A) + 1):
        L_B[i][1] = max(B[0].arrival_time,L_A[i][0] + B[0].w_equal[A[i-1].number])
        steps[1][i][1] = 0
    for i in range (1,len(B) + 1):
        L_A[1][i] = max(A[0].arrival_time, L_B[0][i] + A[0].w_equal[B[i-1].number])
        steps[0][1][i] = 1


    for i in range(1,len(A) + 1):
        for j in range (1,len(B)+1):
            if i != 1:
                costs = [max(A[i-1].arrival_time,L_A[i-1][j] + A[i-1].w_equal[A[i-2].number]),max(A[i-1].arrival_time,L_B[i-1][j] + A[i-1].w_plus[B[j-1].number])]
                L_A[i][j] = min(costs)
                steps[0][i][j] = costs.index(min(costs))
            if j != 1:
                costs1 = [max(B[j-1].arrival_time,L_A[i][j-1] + B[j-1].w_plus[A[i-1].number]),max(B[j-1].arrival_time,L_B[i][j-1] + B[j-1].w_equal[B[j-2].number])]
                L_B[i][j] = min(costs1)
                steps[1][i][j] = costs1.index(min(costs1))
    cost = [L_A[len(A)][len(B)],L_B[len(A)][len(B)]]
    last = cost.index(min(cost))

    path = []
    path.append(last)
    
    i = len(A)
    j = len(B)
    prevstep = steps[last][i][j]

    while(i > 0 or j > 0):
        #print(last,i,j,steps[last][i][j])
        prevstep = steps[last][i][j]
        path.append(int(prevstep))
        if last == 0:
            i -= 1
        else:
            j -= 1
        last = int(prevstep)
    path.pop(len(path) - 1)
    path.reverse()

    numA = 0
    numB = 0
    for num in range(len(A) + len(B)):
        if path[num] == 0:
            A[numA].passingOrder = num
            A[numA].ifChange = 0
            numA += 1
        else:
            B[numB].passingOrder = num
            B[numB].ifChange = 0
            numB += 1
    return A,B

# A = [Vehicle("A_1",3,'A',0,[0,2,7,3,3],[0,3,7,4,4]),Vehicle("A_2",6,'A',2,[7,2,0,2,3],[7,7,0,7,4]),Vehicle("A_3",9,'A',4,[3,3,3,3,0],[4,4,4,4,0])]
# B = [Vehicle("B_1",4,'B',1,[2,0,2,4,3],[3,0,7,5,4]),Vehicle("B_2",7,'B',3,[3,4,2,0,3],[4,5,7,0,4])]
# nldp(A,B)
