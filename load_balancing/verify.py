class given_constant:
    A = []
    S = []
    L = []
    D = []
    def __init__(self, N, T_safe):
        self.N = N
        self.T_safe = T_safe

class decision_var:
    d_plus = []
    d = []
    l = []  #A: 1, B:2
    e = []
    w = []
    ID = []
def myFunc(e):
    return e.passingOrder

def verify(allVeh):  # gg is for given constant, dd is for decision var
    def f2(allVeh):
        isPass = True
        '''print(dd.l)
        print(gg.S)
        print(gg.N)'''
        for i in range(len(allVeh)):
            if allVeh[i].decision_depart[0] > 0 and allVeh[i].scheduled_enter < allVeh[i].decision_depart[0] + 15:
                isPass = False  
        return isPass

    def f3(allVeh):
        isPass = True
        for i in range(len(allVeh)):
            for j in range (len(allVeh[i].lane) - 1):
                if allVeh[i].lane[j+1] != -1 and abs(allVeh[i].lane[j] - allVeh[i].lane[j+1]) > 1:
                    isPass = False
        return isPass
    def f4(allVeh):
        isPass = True
        for i in range(len(allVeh)):
            for j in range(len(allVeh)):
                if i == j:
                    continue
                for k in range(len(allVeh[i].decision_depart)):
                    if allVeh[i].decision_depart[k] > allVeh[j].decision_depart[k] and allVeh[i].lane[k] == allVeh[j].lane[k] and allVeh[i].lane[k+1] != allVeh[i].lane[k] and allVeh[i].decision_depart[k] - allVeh[j].decision_depart[k] < 2 and allVeh[i].lane[k+1] != -1 and allVeh[i].lane[k] != -1:
                        isPass = False
        return isPass
    def f5(allVeh):
        isPass = True
        for i in range(len(allVeh)):
            for j in range(len(allVeh)):
                if i == j:
                    continue
                for k in range(len(allVeh[i].decision_depart)):
                    if allVeh[i].decision_depart[k] < allVeh[j].decision_depart[k] and allVeh[i].lane[k] == allVeh[j].lane[k+1] and allVeh[i].lane[k+1] != allVeh[i].lane[k] and -allVeh[i].decision_depart[k] + allVeh[j].decision_depart[k] < 2:
                        print(k,allVeh[i].ID,allVeh[i].passingOrder,allVeh[i].decision_depart, allVeh[i].lane[k+1],allVeh[i].lane[k])
                        print(k,allVeh[j].ID,allVeh[j].passingOrder,allVeh[j].decision_depart, allVeh[j].lane[k+1],allVeh[j].lane[k])
                        isPass = False
        return isPass

    def f6(allVeh):
        isPass = True
        for i in range(len(allVeh)):
            for j in range(len(allVeh)):
                if i == j:
                    continue
                for k in range(len(allVeh[i].decision_depart) - 1):
                    if allVeh[i].lane[k+1] == allVeh[j].lane[k+1] and allVeh[i].decision_depart[k] > allVeh[j].decision_depart[k] and allVeh[i].decision_depart[k] - allVeh[j].decision_depart[k] < 1:
                        ifPass = False
                        
        return isPass
    
    def f7(allVeh):
        isPass = True
        for i in range(len(allVeh)):
            for k in range(len(allVeh[i].decision_depart) - 1):
                if allVeh[i].decision_depart[k + 1] > 0 and -allVeh[i].decision_depart[k + 1] + allVeh[i].decision_depart[k] < 15:
                    # print(allVeh[i].decision_depart[k + 1],allVeh[i].decision_depart[k])
                    isPass = False
        return isPass


    def f8(allVeh):
        isPass = True
        allVeh.sort(key=myFunc)
        for i in range(len(allVeh)):
            same = -1
            diff = -1
            for j in range(i-1,0,-1):
                if allVeh[i].lane[0] == allVeh[j].lane[0]:
                    same = j
                    break
            for j in range(i-1,0,-1):
                if allVeh[i].leaveLane == allVeh[j].leaveLane:
                    diff = j
                    break
            if same >= 0 and allVeh[i].scheduled_enter < allVeh[same].scheduled_enter + allVeh[same].w_equal[allVeh[i].number]:
                isPass = False
                print(allVeh[i].ID,allVeh[i].passingOrder,allVeh[i].decision_depart, allVeh[i].lane,allVeh[i].scheduled_enter)
                print(allVeh[same].ID,allVeh[same].passingOrder,allVeh[same].decision_depart, allVeh[same].lane,allVeh[same].scheduled_enter )
                for i in range(len(allVeh)):
                    print(allVeh[i].ID,allVeh[i].passingOrder,allVeh[i].decision_depart, allVeh[i].lane,allVeh[i].scheduled_enter,allVeh[i].outLane,allVeh[i].leaveLane)
            if same != diff and diff >= 0:
                if allVeh[i].scheduled_enter < allVeh[diff].scheduled_enter + allVeh[diff].w_plus[allVeh[i].number]:
                    isPass = False
                    print("1")


        return isPass
            

            


    # decide what formulation you want to test
    f = [f2,f3,f4,f5,f6,f7,f8]
    error_list = []
    for i in range(len(f)):
        print('---------------------')
        print(f'in formation_{i+2}')
        isPass = f[i](allVeh)
        if isPass:
            print('pass')
        else:
            print('fail')
            error_list.append(i+2)

    print("error in formulation ", error_list)
        
'''
## example input
gg = given_constant(3,2,1,1,1,1,1,1) 
# (N, M, T_safe, T_det, T_cacc, T_s, T_c, R)
gg.S = [0,1,2]
gg.T_safe = 1
dd = decision_var()
dd.l = [[0,1,1],[0,1,1],[0,1,1]]
dd.t_plus = [[10,0,3],[0,1,2],[6,3,4]]
dd.t_minus = [[0,7,9],[0,12,6],[20,20,4]]
dd.a = [[1,0,1],[0,1,1],[0,0,1]]
dd.c = [[0,0,0],[1,1,1],[1,1,1]]

print(gg.A)
print(gg.N)

verify(allVeh)
'''