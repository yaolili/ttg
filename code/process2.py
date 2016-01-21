#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     process2.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-01-18 13:00:57
# MODIFIED: 2016-01-18 13:00:59

import os
import sys
from os import listdir

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "sys.argv[1]: input candidate path, file with no query content!"
        print "sys.argv[2]: input query.txt!"
        print "sys.argv[3]: output file path!"
        exit()

    f2 = open(sys.argv[2], "r")
    
    dic = {}
    for line in f2:
        qid, content = line.strip().split("\t")
        if qid in dic:
            print "Duplicated qid!"
            exit()
        dic[qid] = content


    files = [f for f in listdir(sys.argv[1])]
    for file in files:
        readPath = sys.argv[1] + file
        writePath = sys.argv[3] + file + ".all"
        
        f1 = open(readPath, "r")
        f3 = open(writePath, "w+")
        print file
        for i, line in enumerate(f1):
            #print i 
            qid, Qid, wid, rank, score, runName, wcontent = line.strip().split("\t")
            if qid in dic:
                f3.write(qid + "\t" + Qid + "\t" + wid + "\t" + rank + "\t" + score + "\t" + runName + "\t" +  wcontent + "\t" + dic[qid] + "\n")
            else:
                print "Error! qid = " + qid + " not found!"
                exit()

    f1.close()
    f2.close()
    f3.close()