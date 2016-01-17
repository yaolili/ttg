#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     coverage.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-01-16 10:56:56
# MODIFIED: 2016-01-16 10:56:58

import os
import sys
import collections
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer

class Coverage:
    def __init__(self, cluster, tweet):
        self.coverage = {}
        for i in range(len(cluster)):
            self.__vector(cluster[i], tweet)
        # print self.coverage
        # print "------"
        
    def getCoverage(self):
        return self.coverage
    
    def __preProcess(self, s):
        tokenizer = RegexpTokenizer(r'\w+') 
        s = tokenizer.tokenize(s) 
        s = [x.lower() for x in s]
        return s
    
    def __vector(self, curCluster, tweet):
        counterSet = []  #curCluster各个wid对应的Counter
        widSet = []      #curCluster各个wid
        all = 0          #分子
        for i in range(len(curCluster)):
            wid = curCluster[i]
            widSet.append(wid)
            wcontent = tweet[wid]
            wcontent = self.__preProcess(wcontent)
            curCounter = collections.Counter(wcontent)
            all += pow(2, len(curCounter)) - 1
            counterSet.append(curCounter)

        #求共现矩阵
        occurence = {}
        for i in range(len(curCluster)):
            for j in range(len(curCluster)):
                if(i == j):
                    continue
                key = str(i) + "-" + str(j)
                occurence[key] = len(counterSet[j]) + len(counterSet[i]) - len(counterSet[i] + counterSet[j]) 
        
        #计算coverage得分
        for i in range(len(counterSet)):
            #curValue为分母
            curValue = pow(2, len(counterSet[i])) - 1
            for j in range(len(counterSet)):
                if i == j:
                    continue
                key = str(i) + "-" + str(j)
                curValue += pow(2, occurence[key]) - 1
            self.coverage[widSet[i]] = float(curValue) / all

if __name__ == "__main__":
    cluster = [[2, 3], [1]]
    tweet = {1:"#RonWeasleyBirthday it s ron weaslei s birthdai the ginger who vomit slug out from hi mouth happi birthdai ron", 2:"happi birthdai ron weaslei", 3:"#WeasleyIsOurKing happi birthdai ron weaslei"}
    covInstance = Coverage(cluster, tweet)
    result = covInstance.getCoverage()
    print result
    
    
