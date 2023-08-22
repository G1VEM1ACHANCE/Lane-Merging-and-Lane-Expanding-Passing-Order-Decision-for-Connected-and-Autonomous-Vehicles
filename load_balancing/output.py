import numpy as np 
import os 
import csv 

def myfunc(e):
    return e[2],e[0],e[1],e[3]

rootdir = "./output"
alllist = []
alllist1 = []
cnt = 0
for subdir in os.scandir(rootdir):
    for num in os.scandir(subdir):
        temp = []
        temp1 = []
        temp2 = []
        for subdirs in os.scandir(num):
            for files in os.scandir(subdirs):
                cnt += 1
                filesplit = files.path.split('/')
                with open(files.path) as openfile:
                    # print(files.path)
                    for line in openfile:
                        if "min" in line:
        #             if ('No' in line) or 'dp' in line or 'greedy' in line or 'nldp' in line:
                            ls = line.split(" ")
                            # temp.append(eval(ls[1]))
                            # temp1.append(eval(ls[2]))
                            # temp2.append(eval(ls[3]))
                # print(filesplit)
                            alllist.append([filesplit[3], eval(filesplit[4]),filesplit[5],eval(ls[1]),eval(ls[2]),eval(ls[3]),eval(ls[4]),eval(ls[5]),eval(ls[6]),eval(ls[7]),eval(ls[8]),eval(ls[9]),eval(ls[10]),eval(ls[11]),eval(ls[12])])

print("cnt" ,cnt,len(alllist))
alllist.sort(key=myfunc)
for i in range(len(alllist)):
    print(alllist[i][2])
print(len(alllist),alllist[0][3])
alllist1 = []
for i in range(0,len(alllist),10):
    target1 = 0
    target2 = 0
    target3 = 0
    for j in range(10):
        print(i,j)
        if i + j >= len(alllist):
            break
        target1 += alllist[i + j][3]
        target2 += alllist[i + j][4]
        target3 += alllist[i + j][5]
    target1 /= 10
    target2 /= 10
    target3 /= 10
    alllist1.append([alllist[i][0],alllist[i][2],target1,target2,target3])

for i in range(0,len(alllist),10):
    target1 = 0
    target2 = 0
    target3 = 0
    for j in range(10):
        if i + j >= len(alllist):
            break
        target1 += alllist[i + j][6]
        target2 += alllist[i + j][7]
        target3 += alllist[i + j][8]
    target1 /= 10
    target2 /= 10
    target3 /= 10
    alllist1.append([alllist[i][0],alllist[i][2],target1,target2,target3])

for i in range(0,len(alllist),10):
    target1 = 0
    target2 = 0
    target3 = 0
    for j in range(10):
        if i + j >= len(alllist):
            break
        target1 += alllist[i + j][9]
        target2 += alllist[i + j][10]
        target3 += alllist[i + j][11]
    target1 /= 10
    target2 /= 10
    target3 /= 10
    alllist1.append([alllist[i][0],alllist[i][2],target1,target2,target3])

with open ("output.csv","w",newline="") as file:
    csvwriter = csv.writer(file)
    csvwriter.writerow(['case','num','MN','FCFS max_delay','last lane change max_delay','out_lane_change max_delay','FCFS mean_delay','last lane change mean_delay','out_lane_change mean_delay','FCFS maxe','last lane change maxe','out_lane_change maxe',"milp time","fcfs time","heuristic time"])
    csvwriter.writerows(alllist)

    csvwriter.writerow(['case','MN','fcfsavg,llcavg','olcavg'])
    csvwriter.writerows(alllist1)
    
            