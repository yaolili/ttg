#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     coverage.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-01-16 10:56:56
# MODIFIED: 2016-01-16 10:56:58

import os
import sys
import numpy as np
import collections
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

class Coverage:
    def __init__(self, curCluster):
    
    def __preProcess(self, s):
        tokenizer = RegexpTokenizer(r'\w+') 
        s = tokenizer.tokenize(s) 
        s = [x.lower() for x in s]
        return s
    
    def __vector(self, s1, s2):
        s3 = s1 + " " + s2

        s1 = self.__preProcess(s1)
        s2 = self.__preProcess(s2)
        s3 = self.__preProcess(s3)
        
        counter1 = collections.Counter(s1)
        counter2 = collections.Counter(s2)
        counter3 = collections.Counter(s3)
        
        aList1 = []
        aList2 = []
        for key in counter3:
            if key in counter1:
                v1 = counter1[key]
            else:
                v1 = 0
            if key in self.docSet:
                smooth = float(self.docSet[key]) / self.totalWords
            else:
                smooth = 0
            
            score1 = (v1 + self.mu * smooth) / (len(s1) + self.mu)
            score2 = (counter3[key] - v1 + self.mu * smooth) / (len(s2) + self.mu)
            if score1 == 0:
                score1 = 0.01
            if score2 == 0:
                score2 = 0.01
            aList1.append(score1)
            aList2.append(score2)
        return aList1, aList2
        
    
