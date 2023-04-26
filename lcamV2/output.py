import numpy as np 
import os 
import csv 

def myfunc(e):
    return e[0],e[1]

rootdir = "./output"
alllist = []
for subdir in os.scandir(rootdir):
    for num in os.scandir(subdir):
        temp = []
        temp1 = []
        temp2 = []
        for files in os.scandir(num):
            filesplit = files.path.split('/')
            with open(files.path) as openfile:
                print(files.path)
                for line in openfile:
                    if ('No' in line) or 'dp' in line or 'greedy' in line or 'nldp' in line:
                        ls = line.split(" ")
                        temp.append(eval(ls[len(ls) - 3].split('\n')[0]))
                        temp1.append(eval(ls[len(ls) - 2].split('\n')[0]))
                        temp2.append(eval(ls[len(ls) - 1].split('\n')[0]))
        alllist.append([filesplit[2], eval(filesplit[3]),temp[0],temp[1],temp[2],temp[3],temp1[0],temp1[1],temp1[2],temp1[3],temp2[0],temp2[1],temp2[2],temp2[3]])

alllist.sort(key=myfunc)

with open ("output.csv","w",newline="") as file:
    csvwriter = csv.writer(file)
    csvwriter.writerow(['case','num','n lane change','greedy','nldp','dp','ndelay','gddelay','nldpdelay','dpdelay','nexec','gdexec','nldpexec','dpexec'])
    csvwriter.writerows(alllist)
            