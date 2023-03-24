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

def verify(gg, dd):  # gg is for given constant, dd is for decision var
    def f2(gg, dd):
        isPass = True
        '''print(dd.l)
        print(gg.S)
        print(gg.N)'''
        for i in range(gg.N):
            if dd.e[i] < gg.A[i] + dd.d_plus[i] - gg.D[i] - 1:
                print(f'{dd.ID[i]} early enter',dd.e[i], gg.A[i] + dd.d_plus[i] - gg.D[i],dd.d[i],dd.d_plus[i])
                isPass = False  
        return isPass

    def f3(gg,dd):
        isPass = True
        for i in range(gg.N):
            if dd.d_plus[i] < dd.d[i] or dd.d[i] < gg.D[i]:
                print(dd.d_plus[i],dd.d[i],gg.D[i])
                print(f'{dd.ID[i]} too fast at decision')
                isPass = False
        return isPass
    def f4(gg,dd):
        isPass = True
        for i in range(gg.N):
            if dd.d_plus[i] > dd.e[i] :
                print(f'{dd.ID[i]} schedule error')
                isPass = False
        return isPass
    def f5(gg,dd):
        isPass = True
        for i in range(gg.N):
            for j in range (gg.N):
                if dd.d_plus[i] > dd.d_plus[j] and dd.l[i] == dd.l[j] and dd.l[i] != gg.S[i]:
                    if dd.d_plus[i] - dd.d_plus[j] < gg.T_safe:
                        print(dd.d_plus[i], dd.d_plus[j] ,gg.T_safe,f'{dd.ID[i]} predecessor too close')
                        isPass = False
        return isPass

    def f6(gg,dd):
        isPass = True
        for i in range(gg.N):
            for j in range (gg.N):
                if dd.d_plus[i] < dd.d_plus[j] and dd.l[i] == dd.l[j] and dd.l[i] != gg.S[i]:
                    if dd.d[j] - dd.d_plus[i] < gg.T_safe:
                        print(f'{dd.ID[i]} follower too close')
                        isPass = False
        return isPass
    
    def f7(gg,dd):
        isPass = True
        for i in range (gg.N):
            if i == 0:
                continue
            if dd.e[i] - dd.e[i - 1] < dd.w[i]:
                print(f'{dd.ID[i]} early enter')
                isPass = False
        return isPass
            

            


    # decide what formulation you want to test
    f = [f2,f3,f4,f5,f6,f7]
    error_list = []
    for i in range(len(f)):
        print('---------------------')
        print(f'in formation_{i+2}')
        isPass = f[i](gg,dd)
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

verify(gg,dd)
'''