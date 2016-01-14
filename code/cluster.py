#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     cluster.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-01-02 19:42:26
# MODIFIED: 2016-01-14 19:15:42
# USAGE: python cluster.py ../data/query.txt ../data/candidate/ 100 corpus.info.txt 1.4 0.15 ../data/result/

import os
import sys
from os import listdir
from formulation import Distance
from textRank import Rank

class Cluster:
    def __init__(self, queryFile, candidatePath, mu, corpusFile, sigma, lamda):
        
        self.query = {}
        self.candidate = candidatePath
        self.tweet = {}
        self.cluster = []
        self.qidWidKL = {}
        self.widWidKL = {}
        self.sigma = sigma      #similarity threshold
        self.lamda = lamda      #cluster threshold
        self.qidWidMax = 0
        self.qidWidMin = 999
        self.widWidMax = 0
        self.widWidMin = 999 
        self.widScore = {}
        self.resultList = []
        
        self.klInstance = Distance(mu, corpusFile)
        print "corpus read done!"
    
        #read query info
        f1 = open(queryFile, "r")
        for line in f1:
            qid, qcontent = line.strip().split("\t")
            self.query[qid] = qcontent
        print "read query info done!"
    
    def write(self, writePath):
        #candidate files
        files = [f for f in listdir(self.candidate)]
        for file in files:
            readPath = self.candidate + file
            writeFile = writePath + file + ".cluster"
            result = open(writeFile, "w+")
            log1 = open(writeFile + ".qidWidKL" , "w+")
            log2 = open(writeFile + ".widWidKL" , "w+")
            with open(readPath, "r") as fin:
                for i, line in enumerate(fin):
                    qid, Qid, wid, rank, score, runName, content = line.strip().split("\t")
                    self.tweet[wid] = content
                    
                    #calculate qidWidKL
                    similarity = self.klInstance.kl(self.query[qid], content)
                    
                    if similarity <= self.sigma:
                        self.qidWidKL[qid+"-"+wid] = similarity
                        if (similarity > self.qidWidMax):
                            self.qidWidMax = similarity
                            #print "self.qidWidMax -> %f" %(similarity)

                        if (similarity < self.qidWidMin):
                            self.qidWidMin = similarity
                            #print "self.qidWidMin -> %f" %(similarity)
                        
                        #calculate widWidKL
                        if not self.cluster:
                            self.cluster.append([wid])
                            self.widWidKL[wid] = []
                        else:
                            self.__clustering(wid)
                            
                    
                    #if (i % 10) == 0:
                    if i == 20:
                        print i
                        print len(self.cluster)
                        print self.cluster
                        
                        for key in self.widWidKL:
                            print key
                            #print len(self.widWidKL[key])
                            #print type(self.widWidKL[key][0])
                            print self.widWidKL[key]
                        print "-------------------"
                        rankInstance = Rank(self.widWidKL, self.widWidMin, self.widWidMax)
                        self.widScore = rankInstance.generate(0.85, 0.01)
                        for i in range(len(self.cluster)):
                            maxScore = 0
                            bestWid = -1
                            for wid in self.cluster[i]:
                                if self.widScore[wid] > maxScore:
                                    maxScore = self.widScore[wid]
                                    bestWid = wid
                            self.resultList.append(bestWid)
                        print self.resultList
                
            #write log file
            # log1.write(str(self.qidWidMin) + "\t" + str(self.qidWidMax) + "\n")
            # for key in self.qidWidKL:
                # score = self.__normalize(self.qidWidKL[key], self.qidWidMax, self.qidWidMin)
                # log1.write(key + "\t" + str(score) + "\n")
            # log2.write(str(self.widWidMin) + "\t" + str(self.widWidMax) + "\n")
            # for key in self.widWidKL:
                # score = self.__normalize(self.widWidKL[key], self.widWidMax, self.widWidMin)
                # log2.write(key + "\t" + str(score) + "\n")
                
            #write cluster    
            for i in range(len(self.cluster)):
                for wid in self.cluster[i]:
                    result.write(wid + "\t" + self.tweet[wid] + "\n\n")
                result.write("----------------------------\n")
            result.close()   
            exit()    
        f1.close()
        
    def __clustering(self, wid):
        maxScore = 999
        index = -1
        wcontent = self.tweet[wid]
        for i in range(len(self.cluster)):          
            for cwid in self.cluster[i]:
                ccontent = self.tweet[cwid]
                score = self.klInstance.kl(self.tweet[wid], self.tweet[cwid])
                #print i
                if wid in self.widWidKL:
                    self.widWidKL[wid].append({cwid: score})
                else:
                    self.widWidKL[wid] = [{cwid: score}]
                
                if cwid in self.widWidKL:
                    self.widWidKL[cwid].append({wid: score})
                else:
                    self.widWidKL[cwid] = [{wid: score}]
                    
                    
                #self.widWidKL[wid+"-"+cwid] = score
                if score < maxScore:
                    maxScore = score
                    index = i
                if score < self.widWidMin:
                    self.widWidMin = score

                if score > self.widWidMax:
                    self.widWidMax = score
                    
        #put wid into the cluster 
        #a new cluster
        if maxScore > self.lamda:
            self.cluster.append([wid])
            #print self.cluster
        #add to a highest similarity cluster
        else:
            self.cluster[index].append(wid)
  
        
    

    
# USAGE: python cluster.py ../data/query.txt ../data/candidate/ 100 corpus.info.txt 1.4 0.15 ../data/result/
if __name__ == '__main__':
    if len(sys.argv) < 8:
        print "sys.argv[1]: input query file!"
        print "sys.argv[2]: input candidate file path!"
        print "sys.argv[3]: input smooth mu!"
        print "sys.argv[4]: input corpus file!"
        print "sys.argv[5]: input similarity threshold!"
        print "sys.argv[6]: input cluster threshold!"
        print "sys.argv[7]: output file path!"
        exit()

    clusterInstance = Cluster(sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4], float(sys.argv[5]), float(sys.argv[6]))
    clusterInstance.write(sys.argv[7])
    
    

    
    
