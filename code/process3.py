#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     process3.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-01-19 20:28:11
# MODIFIED: 2016-01-19 20:28:12

import os
import sys
from os import listdir


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "sys.argv[1]: input trec14.docEx.api.corpus!"
        print "sys.argv[2]: output file path!"
        exit()
    
    f1 = open(sys.argv[1], "r")
    f2 = open(sys.argv[2], "w+")
    for line in f1:
        qid, wid, content = line.strip().split("\t")
        f2.write(content + "\n")

        
    
    
