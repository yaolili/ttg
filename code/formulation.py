#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     formulation.py
# ROLE:     TODO (some explanation)
# CREATED:  2015-12-21 09:08:16
# MODIFIED: 2016-01-20 00:38:55

import numpy as np
import collections
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from w2v import W2V
from scipy import linalg, mat, dot

class Distance:
    def __init__(self, u, corpus):
        #self.w2vInstantce = W2V("w2v.out")
        self.mu = float(u)
        self.docSet = {}
        self.totalWords = 0
        self.stopwords = {}
        with open("/home/yaolili/nltk_data/corpora/stopwords/english", "r")as fin:
            for line in fin:
                word = line.strip().split("\n")
                if word:
                    self.stopwords[word[0]] = 0
                    
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
    
    #unnecessary
    def __stem(self, s):
        s = self.__preProcess(s)
        stem = []
        for w in s:
            stem.append(PorterStemmer().stem(w))
        return stem
    
    def __preProcess(self, s):
        tokenizer = RegexpTokenizer(r'\w+') 
        s = tokenizer.tokenize(s) 
        #s = [x.lower() for x in s]
        s = [w.lower() for w in s if w.lower() not in self.stopwords]
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
        
    def __cosine(self, list1, list2):
        a = mat(list1)
        b = mat(list2)
        c = dot(a,b.T)/linalg.norm(a)/linalg.norm(b)
        return c[0,0]            
    
    def kl(self, s1, s2):
        """Kullback-Leibler divergence D(P || Q) for discrete distributions

        Parameters
        ----------
        p, q : array-like, dtype=float, shape=n
        Discrete probability distributions.
        """
        p, q = self.__vector(s1, s2)
        # print p
        # print q

        p = np.asarray(p, dtype = np.float)
        q = np.asarray(q, dtype = np.float)
        
        k1 = np.sum(np.where(p != 0, p * np.log(p / q), 0))
        k2 = np.sum(np.where(q != 0, q * np.log(q / p), 0))
        return (k1 + k2) / 2
        
        # w2v
        # p = self.w2vInstantce.sentenceVector(s1)
        # q = self.w2vInstantce.sentenceVector(s2)
        # return self.__cosine(p, q)
    
    
if __name__ == "__main__":
        
    s2 = "http://t.co/fWX9kjZz a port in the storm how on professor defi the queensland flood with minecraft kotaku australia a port in the storm how on professor defi the queensland flood with minecraft kotaku australia"
    
    s1 = "cyclon oswald wikipedia free encyclopediaacross affect region damag sever weather flood amount januari australian bureau meteorolog tropic cyclon low pressur system move east queens    land coast flood australia wikipedia free encyclopediathi list notabl record flood occur countri australia eastern australia flood jan qld nsw 6 flood disast hit australia east coast abc new australian jan australia east coast flood disast peopl bundaberg unabl return home citi bbc new major flood crisi hit queensland australiajan australian state queensland face major flood crisi premier warn rescuer reach hundr peopl queensland flood australian red crossaustralian red cross power human recov major disast queensland flood long complex emot journei queensland flood eastern australia flood western australian"
    
    instance = Distance(100, "corpus.info.txt")
    print "__init__ done!"
    print instance.kl(s1, s2)    



 

