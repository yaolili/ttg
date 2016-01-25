#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     jaccard.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-01-18 11:26:16
# MODIFIED: 2016-01-18 11:26:17

import os
import sys
import collections
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer


class Jaccard:
    
    def __preProcess(self, s):
        tokenizer = RegexpTokenizer(r'\w+') 
        s = tokenizer.tokenize(s) 
        s = [x.lower() for x in s]
        return s
        
    def jaccardScore(self, s1, s2):
        s1 = self.__preProcess(s1)
        s2 = self.__preProcess(s2)
        counter1 = collections.Counter(s1)
        counter2 = collections.Counter(s2)
        score = float(len(counter1) + len(counter2) - len(counter1 + counter2)) / len(counter1 + counter2)
        return score
        
if __name__ == "__main__":
    s1 = "it s ron weaslei s birthdai todai thank you for be an awesom ginger and i will forev love you happi birthdai king weaslei"
    s2 = "#Ron #Wesley #potterhead #harrypotter @jk_rowling dear ronald biliu weaslei ron happi birthdai my ginger von von king lt 333"
    jaccInstance = Jaccard()
    print jaccInstance.jaccardScore(s1, s2)