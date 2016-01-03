#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     getQidContent.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-01-02 20:00:58
# MODIFIED: 2016-01-02 20:01:05

import os
import sys

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "sys.argv[1]: input query content file!"
        print "sys.argv[2]: output file!"
        exit()
        

    result = open(sys.argv[2], "w+")
    with open(sys.argv[1], "r")as fin:
        for i, content in enumerate(fin):
            key = str(i + 171)
            result.write(key + "\t" + content)
    result.close()
            
            
