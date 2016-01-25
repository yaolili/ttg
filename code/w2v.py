#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     w2v.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-01-20 09:48:12
# MODIFIED: 2016-01-20 09:48:13
import numpy as np
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer

class W2V:
    def __init__(self, w2vFile):
        self.dict = {}
        self.demension = 200
        with open(w2vFile, "r") as fin:
            for i, line in enumerate(fin):
                aList = line.strip().split(" ")
                if len(aList) < self.demension:
                    continue
                value = []
                for i in range(1, len(aList)):
                    value.append(float(aList[i]))
                self.dict[aList[0]] = value

    def __tmpNumpyArray(self, vectorKey):
        if vectorKey in self.dict:
            tmpList = self.dict[vectorKey]
            array = np.array(tmpList)
            return array
        else:
            array = np.ones(self.demension)
            array = array / 1000000000000
            return array

    def sentenceVector(self, sentence):
        aList = sentence.strip().split(" ")
        if not aList:
            print "sentence split error in Class W2V sentenceVector()!"
            exit()

        arr1 = self.__tmpNumpyArray(aList[0])
        for i in range(1, len(aList)):
            arr2 = self.__tmpNumpyArray(aList[i])
            arr1 = arr1 + arr2
        return (arr1/len(aList)).tolist()


if __name__ == "__main__":       
    s1 = "it s ron weaslei s birthdai todai thank you for be an awesom ginger and i will forev love you happi birthdai king weaslei"

    w2vInstantce = W2V("w2v.out")
    result = w2vInstantce.sentenceVector(s1)
    print result

