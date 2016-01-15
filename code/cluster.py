#-*- coding:utf-8 -*-
# AUTHOR:   yaolili
# FILE:     cluster.py
# ROLE:     TODO (some explanation)
# CREATED:  2016-01-02 19:42:26
# MODIFIED: 2016-01-15 00:31:28
# USAGE: python cluster.py ../data/query.txt ../data/candidate/ 100 corpus.info.txt 1.4 0.15 ../data/result/ 0.01

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
        self.mu = mu
        self.sigma = sigma      #similarity threshold
        self.lamda = lamda      #cluster threshold       
        self.klInstance = Distance(mu, corpusFile)
        print "corpus read done!"
    
        #read query info
        f1 = open(queryFile, "r")
        for line in f1:
            qid, qcontent = line.strip().split("\t")
            self.query[qid] = qcontent
        f1.close()
        print "read query info done!"
    
    def write(self, writePath, yibuson):
        writeFile = writePath + "res.S" + str(self.sigma) + ".L" + str(self.lamda)
        result = open(writeFile, "w+")
        log = open(writePath + "log.S" + str(self.sigma) + ".L" + str(self.lamda), "w+")
        log.write("Qid\tclusterCount\ttweetCount\n")
        log1 = open(writePath + "qidWidKL.S" + str(self.sigma) + ".L" + str(self.lamda), "w+")
        log2 = open(writePath + "widWidKL.S" + str(self.sigma) + ".L" + str(self.lamda), "w+")
        #candidate files
        num = 1
        files = []
        while(num <= 55):
            files.append(str(num) + ".res.content")
            num += 1
        for file in files:
            #remember to make them initial on each query
            self.curQid = -1
            self.cluster = []
            self.qidWidKL = {}
            self.qidWidMax = 0
            self.qidWidMin = 999
            self.widWidKL = {}
            self.widWidMax = 0
            self.widWidMin = 999 
            self.widScore = {}
            self.resultList = []
            readPath = self.candidate + file  
            
            with open(readPath, "r") as fin:
                for i, line in enumerate(fin):
                    qid, Qid, wid, rank, score, runName, content = line.strip().split("\t")
                    
                    #first time selection
                    if(float(score) < 4.6):
                        if not self.cluster:
                            print "break out of 4.6, ", file, " , empty cluster!"
                            exit()
                        break
                        
                    self.tweet[wid] = content
                    self.curQid = qid
                    
                    #calculate qidWidKL
                    similarity = self.klInstance.kl(self.query[qid], content)
                    
                    if similarity <= self.sigma:
                        self.qidWidKL[qid+"-"+wid] = similarity
                        if (similarity > self.qidWidMax):
                            self.qidWidMax = similarity

                        if (similarity < self.qidWidMin):
                            self.qidWidMin = similarity
                        
                        #calculate widWidKL
                        if not self.cluster:
                            self.cluster.append([wid])
                            self.widWidKL[wid] = []
                        else:
                            self.__clustering(wid)
                            
                    
                    if (i % 100) == 0:
                        print file, " => ", i
                
            log1.write(str(self.qidWidMin) + "\t" + str(self.qidWidMax) + "\n")
            for key in self.qidWidKL:
                log1.write(key + "\t" + str(self.qidWidKL[key]) + "\n")
            log2.write(str(self.widWidMin) + "\t" + str(self.widWidMax) + "\n")
            for key in self.widWidKL:
                for i in range(len(self.widWidKL[key])):
                    for widKey in self.widWidKL[key][i]:
                        log2.write(key + "-" + widKey + "\t" + str(self.widWidKL[key][i][widKey]) + "\n")
                        
            rankInstance = Rank(self.widWidKL, self.widWidMin, self.widWidMax)
            self.widScore = rankInstance.generate(0.85, yibuson)
            
            #log info
            clusterCount = len(self.cluster)
            tweetCount = 0
            
            #select one wid from each cluster & log info 
            for i in range(len(self.cluster)):
                maxScore = 0
                bestWid = -1
                tweetCount += len(self.cluster[i])
                for wid in self.cluster[i]:
                    if self.widScore[wid] > maxScore:
                        maxScore = self.widScore[wid]
                        bestWid = wid
                self.resultList.append(bestWid)
            
            #write log info
            log.write("MB" + self.curQid + "\t" + str(clusterCount) + "\t" + str(tweetCount) + "\n")
            
                       
            #write result
            for wid in self.resultList:
                result.write("MB" + self.curQid + "\t" + "Q0\t" + wid + "\t1\t1\tYAO\n")
            
        
    def __clustering(self, wid):
        minScore = 999
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
                    
                    
                #select miniScore, that is the most similar value
                if score < minScore:
                    minScore = score
                    index = i
                if score < self.widWidMin:
                    self.widWidMin = score

                if score > self.widWidMax:
                    self.widWidMax = score
                    
        #put wid into the cluster 
        #a new cluster
        if minScore > self.lamda:
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
    clusterInstance.write(sys.argv[7], float(sys.argv[8]))
    
    

    
    
