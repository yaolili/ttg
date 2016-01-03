#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     process.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-01-02 18:32:04
# MODIFIED: 2016-01-02 19:28:26

import os
import sys
from os import listdir


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "sys.argv[1]: input order file!"
        print "sys.argv[2]: input content file!"
        print "sys.argv[3]: output file path!"
        exit()

    #f1 = open(sys.argv[1], "r")
    f2 = open(sys.argv[2], "r")
    

    dic = {}
    for line in f2:
        qid, wid, content = line.strip().split("\t")
        '''
        print qid
        print wid
        print content
        exit()
        '''
        if wid not in dic:
            dic[wid] = content
        else:
            if content != dic[wid]:
                print "Error! Duplicated wid and different content!"
                exit()

    files = [f for f in listdir(sys.argv[1])]
    for file in files:
        readPath = sys.argv[1] + file
        writePath = sys.argv[3] + file + ".All"
        f1 = open(readPath, "r")
        f3 = open(writePath, "w+")
        for line in f1:
            qid, Qid, wid, rank, score, runName = line.strip().split(" ")
            '''
            print readPath
            print qid
            print Qid
            print wid
            print rank
            print score
            print runName
            exit()
            '''
            if wid in dic:
                f3.write(qid + "\t" + Qid + "\t" + wid + "\t" + rank + "\t" + score + "\t" + runName + "\t" +  dic[wid] + "\n")
            else:
                print "Error! wid = " + wid + " not found!"
                exit()

    f1.close()
    f2.close()
    f3.close()
