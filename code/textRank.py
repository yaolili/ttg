#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     textRank.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-01-19 16:27:54
# MODIFIED: 2016-01-19 23:22:28

import networkx as nx
from coverage import Coverage

class Rank:
    
    def __init__(self, widWidKL, widWidMin, widWidMax):       
        self.result = {}
        D = nx.DiGraph()
        aList = []
        for key in widWidKL:
            for i in range(len(widWidKL[key])):
                for widKey in widWidKL[key][i]:
                    value = self.__normalize(widWidKL[key][i][widKey], widWidMax, widWidMin)
                    aList.append((key, widKey, value))
        
        D.add_weighted_edges_from(aList)
        G = D.to_undirected()
        self.result = nx.pagerank(D, max_iter = 200)
        '''
        #something will be wrong and I don't know why
        maxScore = 0.2
        minScore = 0.001
        for key in self.result:
            value = self.__normalize(self.result[key], maxScore, minScore)
            self.result[key] = value
        '''
        
    def textRank(self):
        return self.result
        
    def combinedCov(self, alpha, cluster, tweet):
        covInstance = Coverage(cluster, tweet)
        covScore = covInstance.getCoverage()
        for key in self.result:
            origin = self.result[key]
            self.result[key] = alpha * origin + (1 - alpha) * covScore[key]
        return self.result
        
    def __normalize(self, origin, max, min):
        if(max == min):
            return 1
        return 1 - (origin - min) / (max - min)
        
        
        
