#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     cluster.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-01-02 19:42:26
# MODIFIED: 2016-01-02 19:42:38
# USAGE: python cluster.py ../data/query.txt ../data/candidate/ 0.85 /index14/plain/origin.corpus ../data/result.txt

import os
import sys
from os import listdir
from formulation import Distance

if __name__ == '__main__':
    if len(sys.argv) < 6:
        print "sys.argv[1]: input query file!"
        print "sys.argv[2]: input candidate file path!"
        print "sys.argv[3]: input clustering sigma!"
        print "sys.argv[4]: input corpus file!"
        print "sys.argv[5]: output file!"
        exit()
        
    dic = {}
    klInstance = Distance(sys.argv[3], sys.argv[4])
    print "corpus read done!"
    exit()
    
    f1 = open(sys.argv[1], "r")
    for line in f1:
        qid, qcontent = line.strip().split("\t")
        dic[qid] = qcontent
    
    files = [f for f in listdir(sys.argv[2])]
    for file in files:
        readPath = sys.argv[2] + file
        with open(readPath, "r") as fin:
            for line in fin:
                qid, Qid, wid, rank, score, runName, content = line.strip().split("\t")
                print dic[qid]
                print "----------"
                print content
                #exit()
                #param: s1, s2, u
                similarity = klInstance.kl(dic[qid], content)
                print similarity
                exit()
            
            
        
    
    f1.close()
