#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     formulation.py
# ROLE:     TODO (some explanation)
# CREATED:  2015-12-21 09:08:16
# MODIFIED: 2015-12-21 09:08:26

import numpy as np
import collections
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
  

class Distance:
    def __init__(self, u, corpus):
        self.mu = float(u)
        self.docSet = {}
        self.totalWords = 0
        with open(corpus, "r")as fin:
            for i, line in enumerate(fin):
                if i == 0:
                    self.totalWords = int(line)
                else:
                    word, num = line.strip().split("\t")
                    self.docSet[word] = int(num)
        '''
        #first version deal with origin corpus
        with open(corpus, "r")as fin:           
            log = open("Distance.log.txt", "w+")
            for i, line in enumerate(fin):
                aList = line.strip().split("\t")
                if len(aList) != 2:
                    log.write(corpus + " , line : " + str(i) + " , content : " + line + "\n")
                else:
                    wid = aList[0]
                    content = aList[1]
                    stemResult = self.__stem(content)
                    
                    for word in stemResult:
                        self.totalWords += 1
                        if word not in self.docSet:
                            self.docSet[str(word)] = 1
                        else:
                            self.docSet[str(word)] += 1
                if (i % 10000) == 0:
                    print i
        
        result = open("corpus.info.txt", "w+")
        result.write(str(self.totalWords) + "\n")
        for key in self.docSet:
            result.write(key + "\t" + str(self.docSet[key]) + "\n")
        log.close()
        result.close()
        '''
                
    def __stem(self, s):
        s = self.__preProcess(s)
        stem = []
        for w in s:
            stem.append(PorterStemmer().stem(w))
        return stem
    
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
        
                
    
    def kl(self, s1, s2):
        """Kullback-Leibler divergence D(P || Q) for discrete distributions

        Parameters
        ----------
        p, q : array-like, dtype=float, shape=n
        Discrete probability distributions.
        """
        p, q = self.__vector(s1, s2)
        #print p
        #print q
        p = np.asarray(p, dtype = np.float)
        q = np.asarray(q, dtype = np.float)
        
        k1 = np.sum(np.where(p != 0, p * np.log(p / q), 0))
        k2 = np.sum(np.where(q != 0, q * np.log(q / p), 0))
        return (k1 + k2) / 2
    
    
if __name__ == "__main__":
        
    s2 = "http://t.co/5AUYw6l3pg mad men season 6 poster don draper s two face teas the mad men season 6 poster teas two side of don mad men season 6 poster don draper s two face teas zap2it"
    
    s1 = "http://t.co/AbdnEQhaFT fantast artwork for new mad men seri poster mad men season 6 poster the two don draper"
    
    instance = Distance(100, "corpus.info.txt")
    print "__init__ done!"
    print instance.kl(s1, s2)    



 

