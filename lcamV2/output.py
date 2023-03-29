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
        for files in os.scandir(num):
            filesplit = files.path.split('/')
            with open(files.path) as openfile:
                print(files.path)
                for line in openfile:
                    if ('No' in line) or 'dp' in line or 'greedy' in line:
                        ls = line.split(" ")
                        temp.append(eval(ls[len(ls) - 1].split('\n')[0]))
        alllist.append([filesplit[2], eval(filesplit[3]),temp[0],temp[1],temp[2]])

alllist.sort(key=myfunc)

with open ("output.csv","w",newline="") as file:
    csvwriter = csv.writer(file)
    csvwriter.writerow(['case','num','n lane change','greedy','dp'])
    csvwriter.writerows(alllist)
            