import test, input
from verify import decision_var, given_constant, verify
import greedyV1
import dpv1
import nldp
import sys
import time
from test import Vehicle

def get_delay(output):
    delay = 0
    for i in range (len(output)):
        delay += output[i]['scheduled_enter'] - output[i]['arrival_time']
    delay /= len(output)
    return delay

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
method = eval(sys.argv[1])
print(method)

A, B = input.deal_input(sys.argv[2])
if method == 0:
    start = time.time()
    A, B = test.FCFS(A,B)
    end = time.time()
    test.lane_change_merge(A,B)
    print("No lane change:",test.output[len(test.output) - 1]['scheduled_enter'],get_delay(test.output),end-start)
elif method == 1:
    start = time.time()
    A, B = greedyV1.FCFS(A,B)
    end = time.time()
    test.lane_change_merge(A,B)
    print("greedy:",test.output[len(test.output) - 1]['scheduled_enter'],get_delay(test.output),end-start)
elif method == 2:
    start = time.time()
    A, B = dpv1.dpv1(A,B)
    end = time.time()
    #print(A,B)
    test.lane_change_merge(A,B)
    #print("aa",test.output)
    print("dp:",test.output[len(test.output) - 1]['scheduled_enter'],get_delay(test.output),end-start)
elif method == 3:
    start = time.time()
    A, B = nldp.nldp(A,B)
    end = time.time()
    test.lane_change_merge(A,B)
    print("nldp:",test.output[len(test.output) - 1]['scheduled_enter'],get_delay(test.output),end-start)

# #test.output.reverse()
#print("aa",test.output)




N = len(test.output)
T_safe = 2

gg = transfor_to_gg(test.output)
dd = transfor_to_dd(test.output)

verify(gg,dd)
   
    
