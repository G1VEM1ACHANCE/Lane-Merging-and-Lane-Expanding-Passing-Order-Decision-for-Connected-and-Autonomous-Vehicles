import test, input
from verify import decision_var, given_constant, verify
from test import Vehicle

def transfor_to_gg(output):   # gg = (N, M, T_safe, T_det, T_cacc, T_s, T_c, R) 
    gg = given_constant(N,T_safe)
    for i in range(N):
        if 'A' in output[i]['ID']:
            gg.S.append('A')
        else:
            gg.S.append('B')
        if output[i]['lane'] == 'A':
            gg.L.append(1)
        else:
            gg.L.append(2)
        
        gg.A.append(output[i]['arrival_time'] + 50)
        gg.D.append(output[i]['arrival_time'] + 30)


    return gg

def transfor_to_dd(output): 
    dd = decision_var()
    for i in range(N):
        dd.d.append(output[i]['decision_arrive'])
        dd.d_plus.append(output[i]['decision_depart'])
        dd.l.append(output[i]['lane'])
        dd.e.append(output[i]['scheduled_enter'])
        dd.ID.append(output[i]['ID'])
        dd.w.append(output[i]['waiting'])
    return dd

#N = ?
#M = 49   position = 0~49
#Tsafe = 1
#Tdet = 6
#Tcacc = 2
#Ts = 1
#Tc = 3
#Ai = ?
#Si = ?
#R = 20


A, B = input.getInput()
# A = [Vehicle("A_1",1,'A'),Vehicle("A_2",2,'A'),Vehicle("A_3",3,'A'),Vehicle("A_4",4,'A'),Vehicle("A_5",16,'A')]
# B = [Vehicle("B_1",1,'B'),Vehicle("B_2",3,'B'),Vehicle("B_3",4,'B'),Vehicle("B_4",5,'B'),Vehicle("B_5",8,'B')]
test.printPos(A)
test.printPos(B)
test.FCFS(A,B)
test.W_init(A,B)

test.lane_change_merge(A,B)

#test.output.reverse()
#print("aa",test.output)



N = len(test.output)
T_safe = 2

gg = transfor_to_gg(test.output)
dd = transfor_to_dd(test.output)

verify(gg,dd)
   
    
