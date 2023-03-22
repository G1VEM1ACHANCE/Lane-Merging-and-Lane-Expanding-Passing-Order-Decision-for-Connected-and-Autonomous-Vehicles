import numpy as np 
from test import Vehicle


def dpv1(A,B):
    D_safe = 4
    NCA = np.zeros([len(A) + 1,len(B) + 1])
    CA = np.zeros([len(A) + 1,len(B) + 1])
    NCB = np.zeros([len(A) + 1,len(B) + 1])
    CB = np.zeros([len(A) + 1,len(B) + 1])

    steps = np.zeros([4,len(A) + 1,len(B) + 1])
    prev = np.zeros([4,len(A) + 1,len(B) + 1,4])




    NCA[1][0] = A[0].arrival_time
    prev[0][1][0][0] = A[0].arrival_time
    CA[1][0] = A[0].arrival_time
    prev[1][1][0][1] = A[0].arrival_time
    NCB[0][1] = B[0].arrival_time
    prev[2][0][1][2] = B[0].arrival_time
    CB[0][1] = B[0].arrival_time
    prev[3][0][1][3] = B[0].arrival_time
    for i in range (2,len(A) + 1):
        cost = [max(A[i-1].arrival_time,NCA[i-1][0] + A[i-1].w_equal[A[i-2].number]),max(A[i-1].arrival_time,CA[i-1][0]+ A[i-1].w_plus[A[i-2].number])]
        idx = cost.index(min(cost))
        NCA[i][0] = min(cost)
        steps[0][i][0] = idx
        prev[0][i][0] = prev[idx][i-1][0]
        prev[0][i][0][0] = min(cost)
        cost1 = [max(A[i-1].arrival_time,NCA[i-1][0] + A[i-1].w_plus[A[i-2].number]),max(A[i-1].arrival_time,CA[i-1][0]+ max(A[i-1].w_equal[A[i-2].number],D_safe))]
        idx = cost1.index(min(cost1))
        CA[i][0] = min(cost1)
        steps[1][i][0] = idx
        prev[1][i][0] = prev[idx][i-1][0]
        prev[1][i][0][1] = min(cost1)
        
    for i in range (2,len(B) + 1):
        cost = [max(B[i-1].arrival_time,NCB[0][i-1] + B[i-1].w_equal[B[i-2].number]),max(B[i-1].arrival_time,CB[0][i-1]+ B[i-1].w_plus[B[i-2].number])]
        idx = cost.index(min(cost)) + 2
        NCB[0][i] = min(cost)
        steps[2][0][i] = idx
        prev[2][0][i] = prev[idx][0][i-1]
        prev[2][0][i][2] = min(cost)
        cost1 = [max(B[i-1].arrival_time,NCB[0][i-1] + B[i-1].w_plus[B[i-2].number]),max(B[i-1].arrival_time,CB[0][i-1]+ max(B[i-1].w_equal[B[i-2].number],D_safe))]
        idx = cost1.index(min(cost1)) + 2
        steps[3][0][i] = idx
        CB[0][i] = min(cost1)
        prev[3][0][i] = prev[idx][0][i-1]
        prev[3][0][i][3] = min(cost1)



    for i in range (1,len(B) + 1):
        cost = [max(A[0].arrival_time,prev[2][0][i][3] + D_safe,NCB[0][i] + A[0].w_plus[B[i-1].number]),max(A[0].arrival_time,CB[0][i] + max(D_safe,A[0].w_equal[B[i-1].number]))]
        idx = cost.index((min(cost))) + 2
        NCA[1][i] = min(cost)
        steps[0][1][i] = idx
        prev[0][1][i] = prev[idx][0][i]
        prev[0][1][i][0] = min(cost)
        cost1 = [max(A[0].arrival_time,NCB[0][i] + max(D_safe,A[0].w_equal[B[i-1].number])),max(A[0].arrival_time,CB[0][i] + max(D_safe,A[0].w_plus[B[i-1].number]))]
        idx = cost1.index(min(cost1)) + 2
        CA[1][i] = min(cost1)
        steps[1][1][i] = idx
        prev[1][1][i] = prev[idx][0][i]
        prev[1][1][i][1] = min(cost1)

        
    for i in range (1,len(A) + 1):
        cost = [max(B[0].arrival_time,prev[0][i][0][1] + D_safe,NCA[i][0] + B[0].w_plus[A[i-1].number]),max(B[0].arrival_time,CA[i][0] + max(D_safe,B[0].w_equal[A[i-1].number]))]
        idx = cost.index((min(cost)))
        NCB[i][1] = min(cost)
        steps[2][i][1] = idx
        prev[2][i][1] = prev[idx][i][0]
        prev[2][i][1][2] = min(cost)
        cost1 = [max(B[0].arrival_time,NCA[i][0] + max(D_safe,B[0].w_equal[A[i-1].number])),max(B[0].arrival_time,CA[i][0] + max(D_safe,B[0].w_plus[A[i-1].number]))]
        idx = cost1.index(min(cost1))
        CB[i][1] = min(cost1)
        steps[3][i][1] = idx
        prev[3][i][1] = prev[idx][i][0]
        prev[3][i][1][3] = min(cost1)
            


    for i in range (1,len(A) + 1):
        for j in range (1,len(B) + 1):
            if (i != 1):
                costs = [max(A[i-1].arrival_time,NCA[i-1][j] + A[i-1].w_equal[A[i-2].number]),max(A[i-1].arrival_time,CA[i-1][j]+ A[i-1].w_plus[A[i-2].number]),max(A[i-1].arrival_time,prev[2][i-1][j][3] + D_safe,NCB[i-1][j] + A[i-1].w_plus[B[j-1].number]),max(A[i-1].arrival_time,CB[i-1][j] + max(D_safe,A[i-1].w_equal[B[j-1].number]))]
                idx = costs.index(min(costs))
                NCA[i][j] = min(costs)
                steps[0][i][j] = idx
                prev[0][i][j] = prev[idx][i-1][j]
                prev[0][i][j][0] = min(cost)

                costs1 = [max(A[i-1].arrival_time,NCA[i-1][j] + A[i-1].w_plus[A[i-2].number]),max(A[i-1].arrival_time,CA[i-1][j]+ max(D_safe,A[i-1].w_equal[A[i-2].number])),max(A[i-1].arrival_time,NCB[i-1][j] + max(D_safe,A[i-1].w_equal[B[j-1].number])),max(A[i-1].arrival_time,CB[i-1][j] + max(D_safe,A[i-1].w_plus[B[j-1].number]))]
                idx = costs1.index(min(costs1))
                CA[i][j] = min(costs1)
                steps[1][i][j] = idx
                prev[1][i][j] = prev[idx][i-1][j]
                prev[1][i][j][1] = min(cost1)
            if (j != 1):    
                costs = [max(B[j-1].arrival_time,prev[0][i][j-1][1] + D_safe,NCA[i][j-1] + B[j-1].w_plus[A[j-1].number]),max(B[j-1].arrival_time,CA[i][j-1] + max(D_safe,B[j-1].w_equal[A[i-1].number])),max(B[j-1].arrival_time,NCB[i][j-1] + B[j-1].w_equal[B[j-2].number]),max(B[j-1].arrival_time,CB[i][j-1]+ B[j-1].w_plus[B[j-2].number])]
                idx = costs.index(min(costs))
                NCB[i][j] = min(costs)
                steps[2][i][j] = idx
                prev[2][i][j] = prev[idx][i][j-1]
                prev[2][i][j][2] = min(cost)

                costs1 = [max(B[j-1].arrival_time,NCA[i][j-1] + max(D_safe,B[j-1].w_equal[A[i-1].number])),max(B[j-1].arrival_time,CA[i][j-1] + max(D_safe,B[j-1].w_plus[A[i-1].number])),max(B[j-1].arrival_time,NCB[i][j-1] + B[j-1].w_plus[B[j-2].number]),max(B[j-1].arrival_time,CB[i][j-1]+ max(D_safe,B[j-1].w_equal[B[j-2].number]))]
                idx = costs1.index(min(costs1))
                CB[i][j] = min(costs1)
                steps[3][i][j] = idx
                prev[3][i][j] = prev[idx][i][j-1]
                prev[3][i][j][3] = min(cost1)
        
    i = len(A)
    j = len(B)
    cost = [NCA[i][j],CA[i][j],NCB[i][j],CB[i][j]]
    last = cost.index(min(cost))
    prevstep = steps[last][i][j]
    path = []
    path.append(last)
    while(i > 0 or j > 0):
        #print(last,i,j,steps[last][i][j])
        prevstep = steps[last][i][j]
        path.append(int(prevstep))
        if last == 0 or last == 1:
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
        elif path[num] == 1:
            A[numA].passingOrder = num
            A[numA].ifChange = 1
            numA += 1
        elif path[num] == 2:
            B[numB].passingOrder = num
            B[numB].ifChange = 0
            numB += 1
        elif path[num] == 3:
            B[numB].passingOrder = num
            B[numB].ifChange = 1
            numB += 1
    # for i in range(len(A)):
    #     print(A[i].passingOrder,B[i].passingOrder)
    print(path)
    return A,B

        

        
        


    print(path)
    print(NCA,'\n',steps[0][:][:])
    print(CA,'\n',steps[1][:][:])
    print(NCB,'\n',steps[2][:][:])
    print(CB,'\n',steps[3][:][:])


# A = [Vehicle("A_1",3,'A',0,[0,2,7,3,3],[0,3,7,4,4]),Vehicle("A_2",6,'A',2,[7,2,0,2,3],[7,7,0,7,4]),Vehicle("A_3",9,'A',4,[3,3,3,3,0],[4,4,4,4,0])]
# B = [Vehicle("B_1",4,'B',1,[2,0,2,4,3],[3,0,7,5,4]),Vehicle("B_2",7,'B',3,[3,4,2,0,3],[4,5,7,0,4])]
# dpv1(A,B)

