#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     textRank.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-01-14 13:29:51
# MODIFIED: 2016-01-14 20:19:56

from coverage import Coverage


class Rank:
    def __init__(self, widWidKL, widWidMin, widWidMax, cluster, tweet):
        self.score = {}            #wid - current score
        self.widWidKL = widWidKL   #wid - wid similarity score
        self.widTotal = {}         #wid - total score
        
        covInstance = Coverage(cluster, tweet)
        self.covScore = covInstance.getCoverage()
        
        for key in widWidKL:
            self.score[key] = self.covScore[key]
            #self.score[key] = 1
            self.widTotal[key] = 0
            for i in range(len(widWidKL[key])):
                for widKey in widWidKL[key][i]:
                    value = self.__normalize(widWidKL[key][i][widKey], widWidMax, widWidMin)
                    self.widWidKL[key][i][widKey] = value
                    self.widTotal[key] += self.widWidKL[key][i][widKey]

    def __normalize(self, origin, max, min):
        if(max == min):
            return 1
        return 1 - (origin - min) / (max - min)
        
    def generate(self, d, yibuson, alpha, beta):
        flag = True
        iterTime = 1
        while(flag):
            print "iterTime: ", iterTime
            iterTime += 1
            count = 0
            for key in self.widWidKL:
                tmp = 0
                for i in range(len(self.widWidKL[key])):
                    for widKey in self.widWidKL[key][i]:
                        tmp += self.widWidKL[key][i][widKey] / self.widTotal[widKey] * self.score[widKey]
                        
                #newScore = alpha * ((1 - d) + d * tmp) + (1 - alpha) * (beta * self.score[key] + (1 - beta) * self.covScore[key])
                newScore = alpha * ((1 - d) + d * tmp) + (1 - alpha) * (beta + (1 - beta) * self.covScore[key]) 
                #newScore = (1 - d) + d * tmp 
                if abs(newScore - self.score[key]) < yibuson:
                    count += 1
                self.score[key] = newScore
            if count == len(self.score):
                flag = False
        return self.score
            
